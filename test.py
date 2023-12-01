from datetime import datetime

import pytest

from main import MutualFundCalculator

# Test data
mock_nav_data = [
    {"date": "08-04-2006", "nav": "37.49230"},
    {"date": "07-04-2006", "nav": "378.57640"},
    {"date": "06-04-2006", "nav": "300.08770"},
    {"date": "05-04-2006", "nav": "31.66920"},
    {"date": "04-04-2006", "nav": "370.42310"},
    {"date": "03-04-2006", "nav": "35.44000"},
    {"date": "02-04-2006", "nav": "321.81810"},
    {"date": "01-04-2006", "nav": "3716.46800"},
]


def test_convert_nav_data():
    nav_dict = MutualFundCalculator.convert_nav_data(mock_nav_data)
    assert isinstance(nav_dict, dict)
    assert len(nav_dict) == len(mock_nav_data)
    assert isinstance(list(nav_dict.keys())[0], datetime)
    assert isinstance(list(nav_dict.values())[0], float)


def test_find_nearest_date():
    # Test finding nearest date in NAV data
    nav_data = {
        datetime.strptime(entry["date"], "%d-%m-%Y"): float(entry["nav"])
        for entry in mock_nav_data
    }
    nearest_date = MutualFundCalculator.find_nearest_date(
        nav_data, datetime(2006, 4, 6)
    )
    assert nearest_date == datetime(2006, 4, 6)


def test_calculate_profit():
    # Test calculating mutual fund profit
    scheme_code = "123456"
    start_date = "08-04-2006"
    end_date = "04-04-2006"
    capital = 100000.0

    def mock_get_nav_for_date_range(scheme_code, start_date, end_date):
        return mock_nav_data

    MutualFundCalculator.get_nav_for_date_range = mock_get_nav_for_date_range

    profit = MutualFundCalculator.calculate_profit(
        scheme_code, start_date, end_date, capital
    )
    assert profit == 887997.8022153882


if __name__ == "__main__":
    pytest.main(["-v"])
