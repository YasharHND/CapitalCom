#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from capitalcom import Client
from capitalcom.client_demo import Client as DemoClient

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables with fallback to dummy values
api_key = os.environ.get("CAPITAL_API_KEY", "your_api_key")
email = os.environ.get("CAPITAL_EMAIL", "your_email")
password = os.environ.get("CAPITAL_API_KEY_CUSTOM_PASSWORD", "your_password")
use_demo = os.environ.get("CAPITAL_USE_DEMO", "false").lower() == "true"


def get_gold_price():
    try:
        # Initialize appropriate client (demo or live)
        if use_demo:
            print("Using demo client")
            client = DemoClient(email, password, api_key)
        else:
            print("Using live client")
            client = Client(email, password, api_key)

        # Get market details for gold directly using its epic
        gold_epic = "GOLD"
        gold_data = client.single_market(epic=gold_epic)
        print(f"Gold market data retrieved for epic: {gold_epic}")

        # Extract and display the price
        if "snapshot" in gold_data and "bid" in gold_data["snapshot"]:
            print(f"Current gold price (bid): {gold_data['snapshot']['bid']}")
        if "snapshot" in gold_data and "offer" in gold_data["snapshot"]:
            print(f"Current gold price (ask): {gold_data['snapshot']['offer']}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    get_gold_price()
