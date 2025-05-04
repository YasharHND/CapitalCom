from capitalcom import client
from capitalcom.client import Client as LiveClient
from capitalcom.client_demo import Client as DemoClient
import os


def fetch_gold_price():
    # Load credentials from environment variables
    api_key = os.environ.get("CAPITAL_API_KEY")
    email = os.environ.get("CAPITAL_EMAIL")
    password = os.environ.get("CAPITAL_API_KEY_CUSTOM_PASSWORD")
    use_demo = os.environ.get("CAPITAL_USE_DEMO", "false").lower() == "true"

    # Validate that all required credentials are present
    if not all([api_key, email, password]):
        return {
            "error": "Missing required environment variables. Please set CAPITAL_API_KEY, CAPITAL_EMAIL, and CAPITAL_API_KEY_CUSTOM_PASSWORD"
        }

    try:
        # Create client instance based on demo flag
        ClientClass = DemoClient if use_demo else LiveClient
        cap_client = ClientClass(email, password, api_key)

        # Gold's epic ID in Capital.com is "GOLD" - we'll fetch its market information
        gold_info = cap_client.single_market("GOLD")

        return {
            "symbol": gold_info["instrument"]["symbol"],
            "currency": gold_info["instrument"]["currency"],
            "bid": gold_info["snapshot"]["bid"],
            "offer": gold_info["snapshot"]["offer"],
        }

    except Exception as e:
        return {"error": str(e)}
