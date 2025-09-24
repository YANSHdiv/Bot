import logging
import sys
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Configure logging
logging.basicConfig(
    filename='bot.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BINANCE_TESTNET_URL = "https://testnet.binancefuture.com"

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        if testnet:
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.FUTURES_URL = BINANCE_TESTNET_URL
        else:
            self.client = Client(api_key, api_secret)
        logging.info("Bot initialized (testnet={})".format(testnet))

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            order_params = {
                "symbol": symbol.upper(),
                "side": SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                "quantity": quantity,
                "type": order_type
            }
            if order_type == ORDER_TYPE_LIMIT:
                order_params["price"] = price
                order_params["timeInForce"] = TIME_IN_FORCE_GTC
            if order_type == ORDER_TYPE_STOP_MARKET:
                order_params["stopPrice"] = stop_price
            if order_type == ORDER_TYPE_STOP_LIMIT:
                order_params["stopPrice"] = stop_price
                order_params["price"] = price
                order_params["timeInForce"] = TIME_IN_FORCE_GTC
            logging.info(f"Placing order: {order_params}")
            order = self.client.futures_create_order(**order_params)
            logging.info(f"Order response: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Binance API error: {e}")
            print("Order failed:", e)
            return None
        except Exception as e:
            logging.error(f"Other error: {e}")
            print("Order failed:", e)
            return None

def get_input(prompt, validator=str.strip, required=True):
    while True:
        try:
            value = validator(input(prompt))
            if not value and required:
                print("Input required.")
                continue
            return value
        except Exception as e:
            print("Invalid input:", e)

def main():
    print("=== Binance Futures Testnet Trading Bot ===")
    api_key = get_input("Enter API Key: ")
    api_secret = get_input("Enter API Secret: ")
    bot = BasicBot(api_key, api_secret)

    while True:
        print("\nAvailable order types:\n1. MARKET\n2. LIMIT\n3. STOP_MARKET\n4. STOP_LIMIT")
        order_type = get_input("Enter order type: ", str.upper)
        symbol = get_input("Symbol (e.g. BTCUSDT): ", str.upper)
        side = get_input("Side (buy/sell): ", str.lower)
        quantity = float(get_input("Quantity: ", float))
        price = None
        stop_price = None

        if order_type in [ORDER_TYPE_LIMIT, ORDER_TYPE_STOP_LIMIT]:
            price = float(get_input("Limit price: ", float))
        if order_type in [ORDER_TYPE_STOP_MARKET, ORDER_TYPE_STOP_LIMIT]:
            stop_price = float(get_input("Stop price: ", float))

        result = bot.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        if result:
            print("Order placed successfully:", result)
        else:
            print("Order failed. See 'bot.log' for details.")

        more = get_input("Place another order? (y/n): ", str.lower)
        if more != 'y':
            break

if __name__ == "__main__":
    main()
