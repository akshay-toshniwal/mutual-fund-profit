# mutual-fund-profit

This is a FastApi bases web application which is used to calculate the profit for a mutual fund investment from nav.

## Prerequisites

- Python 3.x
- pip
- virtualenv (optional, but recommended)

### Install virtualenv if not already installed
  ```
  pip install virtualenv
```
### Create a virtual environment (replace 'venv' with your preferred name)
```
  virtualenv venv
```
### Activate the virtual environment

  #### On Windows:
```
  venv\Scripts\activate
```
  #### On macOS and Linux:
```
  source venv/bin/activate
```
## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/akshay-toshniwal/mutual-fund-profit.git
   cd mutual-fund-profit
   ```   
2. To start with project
    ```
    cd mutual-fund-profit/
    ```

3. Install Django and project dependencies:

   ```
   pip install -r requirements.txt
   ```

6. Run the development server:

   ```
   uvicorn main:app --reload
   ```

7. Access the application in your web browser at http://localhost:8000/

8. Run tests using

```
pytest test.py
```

9. Follows PEP8 standars with linting tools

```
flake8 .
black .
isort .
```
