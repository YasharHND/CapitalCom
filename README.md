# CapitalCom

A simple Python project to interact with Capital.com's API.

## Project Structure

```
├── src/
│   └── fetch_gold_price.py    # Module for fetching gold price data
└── notebooks/
    └── FetchGoldPrice.ipynb   # Jupyter notebook for testing and development
```

## Features

- Fetch real-time gold prices from Capital.com API
- Support for both live and demo API environments
- Clean data output with essential price information:
  - Symbol
  - Currency
  - Bid price
  - Offer price

## Environment Variables

The following environment variables are required:

- `CAPITAL_API_KEY`: Your Capital.com API key
- `CAPITAL_EMAIL`: Your Capital.com account email
- `CAPITAL_API_KEY_CUSTOM_PASSWORD`: Your Capital.com API password
- `CAPITAL_USE_DEMO`: Set to "true" for demo environment, "false" for live (optional, defaults to "false")

## Usage

```python
from src.fetch_gold_price import fetch_gold_price

# Returns a dictionary with current gold price information
result = fetch_gold_price()
# {
#     "symbol": "Gold",
#     "currency": "USD",
#     "bid": 3240.93,
#     "offer": 3241.23
# }
```

## Dependencies

- capitalcom-python
- python-dotenv (for development)
