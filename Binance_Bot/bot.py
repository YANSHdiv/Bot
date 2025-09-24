import logging
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

# Configure logging
logging.basicConfig(
    filename='bot.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BINANCE_TESTNET_URL = "https://testnet.binancefuture.com"

# UI Style
ui_style = Style.from_dict({
    'title': '#00aa00 bold',
    'prompt': '#ffffff bold',
    'success': '#00ff00',
    'error': '#ff0000',
    'info': '#00aaff',
})

# Auto-completion for common trading pairs
symbol_completer = WordCompleter([
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT', 
    'SOLUSDT', 'DOGEUSDT', 'DOTUSDT', 'AVAXUSDT', 'MATICUSDT'
])

order_type_completer = WordCompleter(['MARKET', 'LIMIT', 'STOP_MARKET', 'STOP'])
side_completer = WordCompleter(['buy', 'sell'])

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
                "side": "BUY" if side.lower() == "buy" else "SELL",
                "quantity": quantity,
                "type": order_type.upper()
            }
            if order_type.upper() == "LIMIT":
                order_params["price"] = price
                order_params["timeInForce"] = "GTC"
            elif order_type.upper() == "STOP_MARKET":
                order_params["stopPrice"] = stop_price
            elif order_type.upper() == "STOP":
                order_params["stopPrice"] = stop_price
                order_params["price"] = price
                order_params["timeInForce"] = "GTC"
            
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

def get_styled_input(message, completer=None, password=False, validator=None):
    """Enhanced input with styling and auto-completion"""
    try:
        if password:
            return prompt(HTML(f'<prompt>{message}</prompt>'), 
                         style=ui_style, is_password=True)
        else:
            return prompt(HTML(f'<prompt>{message}</prompt>'), 
                         completer=completer, style=ui_style)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

def get_float_input(message):
    """Get float input with validation"""
    while True:
        try:
            value = get_styled_input(message)
            return float(value)
        except ValueError:
            print(HTML('<error>❌ Please enter a valid number</error>'))

def print_styled(message, style_class='info'):
    """Print styled messages"""
    from prompt_toolkit import print_formatted_text
    print_formatted_text(HTML(f'<{style_class}>{message}</{style_class}>'), style=ui_style)

def show_welcome():
    """Display welcome screen"""
    from prompt_toolkit import print_formatted_text
    print_formatted_text(HTML('<title>🚀 === Binance Futures Testnet Trading Bot === 🚀</title>'), style=ui_style)
    print_formatted_text(HTML('<info>📊 Advanced trading interface with auto-completion</info>'), style=ui_style)
    print_formatted_text(HTML('<info>⚡ Fast order execution on Binance testnet</info>'), style=ui_style)
    print("-" * 60)

def main():
    show_welcome()
    
    # Get API credentials with enhanced input
    print_styled("🔐 Please enter your Binance testnet credentials:", "title")
    api_key = get_styled_input("🔑 Enter API Key: ", password=True)
    api_secret = get_styled_input("🔒 Enter API Secret: ", password=True)
    
    print_styled("✅ Connecting to Binance testnet...", "success")
    bot = BasicBot(api_key, api_secret)
    
    while True:
        print_styled("\n📈 === New Order === 📈", "title")
        print_styled("Available order types: MARKET | LIMIT | STOP_MARKET | STOP", "info")
        
        # Get order details with auto-completion
        order_type = get_styled_input("📋 Enter order type: ", order_type_completer).upper()
        symbol = get_styled_input("💰 Symbol (e.g. BTCUSDT): ", symbol_completer).upper()
        side = get_styled_input("📊 Side (buy/sell): ", side_completer).lower()
        quantity = get_float_input("🔢 Quantity: ")
        
        price = None
        stop_price = None

        if order_type in ["LIMIT", "STOP"]:
            price = get_float_input("💵 Limit price: ")
        if order_type in ["STOP_MARKET", "STOP"]:
            stop_price = get_float_input("🛑 Stop price: ")

        # Confirm order
        print_styled(f"\n📝 Order Summary:", "info")
        print_styled(f"   Symbol: {symbol}", "info")
        print_styled(f"   Side: {side.upper()}", "info")
        print_styled(f"   Type: {order_type}", "info")
        print_styled(f"   Quantity: {quantity}", "info")
        if price:
            print_styled(f"   Price: {price}", "info")
        if stop_price:
            print_styled(f"   Stop Price: {stop_price}", "info")
        
        if confirm(HTML('<prompt>🚀 Execute this order?</prompt>'), style=ui_style):
            result = bot.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )
            if result:
                print_styled("✅ Order placed successfully!", "success")
                print_styled(f"Order ID: {result.get('orderId', 'N/A')}", "success")
            else:
                print_styled("❌ Order failed. Check 'bot.log' for details.", "error")
        else:
            print_styled("❌ Order cancelled.", "info")

        if not confirm(HTML('<prompt>📈 Place another order?</prompt>'), style=ui_style):
            print_styled("👋 Thanks for using the trading bot!", "success")
            break

if __name__ == "__main__":
    main()
