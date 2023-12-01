import logging
from datetime import datetime, timedelta

import requests
from fastapi import FastAPI, Query

app = FastAPI()

logging.basicConfig(level=logging.INFO)


class MutualFundCalculator:
    @staticmethod
    def convert_nav_data(nav_data):
        """Converts fetched NAV data to a dictionary.

        Args:
        nav_data (list): List of dictionaries containing 'date' and 'nav' keys.

        Returns:
        dict: A dictionary mapping dates to NAV values.
        """
        return {
            datetime.strptime(entry["date"], "%d-%m-%Y"): float(entry["nav"])
            for entry in nav_data
        }

    @staticmethod
    def get_nav_for_date_range(scheme_code: str, start_date: str, end_date: str):
        """Fetches NAV data for the given date range.

        Args:
        scheme_code (str): The unique scheme code of the mutual fund.
        start_date (str): The start date of the date range in 'dd-mm-yyyy' format.
        end_date (str): The end date of the date range in 'dd-mm-yyyy' format.

        Returns:
        list: List of dictionaries containing NAV data for the specified date range.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
                               AppleWebKit/537.36 (KHTML, like Gecko) \
                               Chrome/118.0.0.0 Safari/537.36"
            }
            response = requests.get(
                f"https://api.mfapi.in/mf/{scheme_code}?\
                  start={start_date}&end={end_date}",
                headers=headers,
            )
            if response.status_code == 200:
                logging.info(f"Successfully fetched Nav data {response.status_code}")
                return response.json()["data"]
        except Exception as e:
            logging.error(
                f"ERROR: {response.status_code} | Failed fetching NAV data: {e}"
            )
        return []

    @staticmethod
    def find_nearest_date(nav_data, target_date):
        """Finds the nearest available date in the fetched NAV data.

        Args:
        nav_data (dict): Dictionary mapping dates to NAV values.
        target_date (datetime): The target date to find in the NAV data.

        Returns:
        datetime: The nearest available date in the NAV data.
        """
        while target_date not in nav_data:
            target_date += timedelta(days=1)
        return target_date

    @staticmethod
    def calculate_profit(
        scheme_code: str, start_date: str, end_date: str, capital: float = 1000000.0
    ) -> float:
        """Calculates the mutual fund profit.

        Args:
        scheme_code (str): The unique scheme code of the mutual fund.
        start_date (str): The purchase date of the mutual fund in 'dd-mm-yyyy' format.
        end_date (str): The redemption date of the mutual fund in 'dd-mm-yyyy' format.
        capital (float, optional): The initial investment amount (default: 1000000.0).

        Returns:
        float: The calculated net profit.
        """
        try:
            start = datetime.strptime(start_date, "%d-%m-%Y")
            end = datetime.strptime(end_date, "%d-%m-%Y")

            fetched_nav_data = MutualFundCalculator.get_nav_for_date_range(
                scheme_code, start, end
            )

            if not fetched_nav_data:
                return 0.0

            nav_data = MutualFundCalculator.convert_nav_data(fetched_nav_data)

            start = MutualFundCalculator.find_nearest_date(nav_data, start)
            end = MutualFundCalculator.find_nearest_date(nav_data, end)

            start_nav = float(nav_data[start])
            end_nav = float(nav_data[end])

            units_allotted = capital / start_nav
            value_at_redemption = units_allotted * end_nav
            net_profit = value_at_redemption - capital
            return net_profit

        except Exception as e:
            logging.error(f"Error calculating profit: {e}")

        return 0.0


@app.get("/profit")
async def calculate_profit(
    scheme_code: str = Query(
        ..., description="The unique scheme code of the mutual fund."
    ),
    start_date: str = Query(
        ..., description="The purchase date of the mutual fund (dd-mm-yyyy)."
    ),
    end_date: str = Query(
        ..., description="The redemption date of the mutual fund (dd-mm-yyyy)."
    ),
    capital: float = Query(1000000.0, description="The initial investment amount."),
):
    """Endpoint to calculate mutual fund profit.

    Args:
    scheme_code (str): The unique scheme code of the mutual fund.
    start_date (str): The purchase date of the mutual fund in 'dd-mm-yyyy' format.
    end_date (str): The redemption date of the mutual fund in 'dd-mm-yyyy' format.
    capital (float, optional): The initial investment amount (default: 1000000.0).

    Returns:
    dict: A dictionary containing the calculated net profit.
    """

    mf_calculator = MutualFundCalculator()
    profit = mf_calculator.calculate_profit(scheme_code, start_date, end_date, capital)
    return {"net_profit": profit}
