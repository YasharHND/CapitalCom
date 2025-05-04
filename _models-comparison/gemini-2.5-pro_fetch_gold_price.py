import os
from dotenv import load_dotenv

# Conditionally import the correct client
# We assume 'capitalcom.client' exists for the live environment
try:
    from capitalcom.client import Client as LiveClient
except ImportError:
    # Fallback or handle cases where only one client type might be installed/relevant
    LiveClient = None
    print(
        "Warning: Live client ('capitalcom.client.Client') not found. Only demo mode is available."
    )

from capitalcom.client_demo import Client as DemoClient


# Load environment variables from .env file
load_dotenv()

# --- Configuration from Environment Variables ---
API_KEY = os.getenv("CAPITAL_API_KEY")
IDENTIFIER = os.getenv("CAPITAL_EMAIL")
PASSWORD = os.getenv("CAPITAL_API_KEY_CUSTOM_PASSWORD")
# Check if we should use the demo environment (treat anything other than 'false' as true for safety)
USE_DEMO_STR = os.getenv("CAPITAL_USE_DEMO", "true").lower()
USE_DEMO = USE_DEMO_STR != "false"

# Validate required environment variables
if not all([API_KEY, IDENTIFIER, PASSWORD]):
    print("Error: Missing required environment variables:")
    if not API_KEY:
        print("- CAPITAL_API_KEY")
    if not IDENTIFIER:
        print("- CAPITAL_EMAIL")
    if not PASSWORD:
        print("- CAPITAL_API_KEY_CUSTOM_PASSWORD")
    exit(1)  # Exit if configuration is incomplete

# Select Base URL and Client based on USE_DEMO flag
if USE_DEMO:
    BASE_URL = "https://demo-api-capital.backend-capital.com/"
    ClientClass = DemoClient
    print("Using DEMO environment.")
else:
    if LiveClient is None:
        print("Error: Cannot use live environment because LiveClient failed to import.")
        exit(1)
    BASE_URL = "https://api-capital.backend-capital.com/"  # Live environment URL
    ClientClass = LiveClient
    print("Using LIVE environment.")


def get_gold_price():
    """
    Fetches the current gold price from Capital.com demo API.

    Returns:
        dict: A dictionary containing market details for gold, or None if an error occurs.
    """
    try:
        # Initialize the client with required credentials
        client = ClientClass(log=IDENTIFIER, pas=PASSWORD, api_key=API_KEY)

        # --- Authentication ---
        # Assuming session is handled internally by the client initialization
        # Check if the client object seems valid (simple check)
        # The previous check for cst/security_token failed, let's rely on the API call to fail if auth is wrong.
        print("Client initialized. Attempting API call...")

        # --- Fetch Gold Market Details using EPIC ---
        market_epic = "GOLD"
        print(f"Fetching market details for EPIC: {market_epic}...")

        try:
            # Use the discovered 'single_market' method with the EPIC
            market_details = client.single_market(market_epic)

            if (
                market_details
                and "snapshot" in market_details
                and "bid" in market_details["snapshot"]
            ):
                print(f"Successfully fetched details for {market_epic}.")
                return market_details
            else:
                print(f"Warning: Received unexpected data structure for {market_epic}.")
                print("Response:", market_details)
                # Attempt fetching all markets to find the correct symbol or structure
                # all_markets = client.get_market_details_all()
                # print("All Markets (sample):", str(all_markets)[:500]) # Print first 500 chars
                return None

        except AttributeError:
            print(
                f"Error: The method 'single_market' (or similar taking an EPIC) was not found in the client."
            )
            print(
                "Please check the capitalcom-python library's documentation or source code for the correct method name."
            )
            # You might need to inspect the client object: print(dir(client))
            return None
        except Exception as e:
            print(
                f"An error occurred while fetching market details for {market_epic}: {e}"
            )
            return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # This could be due to invalid credentials, network issues, or API changes.
        return None


if __name__ == "__main__":
    print(
        f"Attempting to fetch Gold price from Capital.com {'Demo' if USE_DEMO else 'Live'} API..."
    )
    gold_data = get_gold_price()

    if gold_data:
        # Extract relevant price information (e.g., bid, ask, last traded)
        # The exact structure depends on the API response
        snapshot = gold_data.get("snapshot", {})
        bid_price = snapshot.get("bid")
        ask_price = snapshot.get("ask")
        # Other potential fields: lastTradedPrice, high, low, netChange, percentageChange

        print("--- Gold Price Snapshot ---")
        if bid_price is not None:
            print(f"Bid Price: {bid_price}")
        if ask_price is not None:
            print(f"Ask Price: {ask_price}")
        # Print other details if available and needed
        # print(f"Full Snapshot: {snapshot}")
    else:
        print("Could not retrieve Gold price data.")

    # Note: Sessions expire after 10 minutes of inactivity.
    # For long-running scripts, session renewal logic would be needed.
    # The library might handle this internally, or require explicit calls.
