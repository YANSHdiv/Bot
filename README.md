# Binance Futures Testnet Trading Bot

A simplified trading bot implemented in Python to place market, limit, stop-market, and stop-limit orders on Binance USDT-M Futures Testnet. This bot demonstrates basic trading functionality using the official Binance API and python-binance library.

---

## Features

- Connects to Binance Futures Testnet (USDT-M) with API keys
- Place Buy and Sell orders with four supported order types
- Interactive command-line interface for user input
- Input validation and error handling
- Logging of API requests and responses to `bot.log`

---

## Prerequisites

- Python 3.8 or above
- Binance Futures Testnet account with API key and secret
- Install required packages:


---

## Setup

1. Register or log into Binance Futures Testnet:  
   [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

2. Generate your API key and secret on the Testnet

3. Clone this repository and navigate to project directory

4. Run the bot:


---

## Usage

- Run the bot script.
- Enter your Binance Testnet API Key and Secret.
- Follow the command prompts to place market, limit, stop-market, or stop-limit orders.
- Inputs are validated; errors are logged.
- Order responses and statuses are printed.
- Logs are saved in `bot.log` in the working directory.

---

## Notes

- This bot works on Binance Futures Testnet only—do NOT use your real account keys here.
- Always test with small quantities and on the Testnet before live trading.
- The `python-binance` library handles Binance API communications.
- Make sure you have stable internet connection while using the bot.

---

## Extending the Bot

You can extend this bot by:

- Adding support for more complex order types such as OCO or TWAP
- Implementing automated trading strategies
- Adding proper asynchronous handling with websockets for real-time data
- Building a more advanced user interface

---

## Troubleshooting

If you encounter issues:

- Check that API keys are generated on Binance Futures Testnet, not Mainnet
- Ensure the testnet base URL is correctly set in the code (`https://testnet.binancefuture.com`)
- Review `bot.log` for detailed error messages
- Verify your system time is synchronized (Binance API requires accurate timestamps)

---

## License

This project is open-source under the MIT License.

---

Happy Trading! 🚀

