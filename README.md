# Binance Futures Trading Bot

A Python CLI application to place MARKET and LIMIT orders on Binance Futures Testnet (USDT-M). Built with a clean, modular structure — separate API client layer, order logic, input validation, and CLI interface — with structured logging and error handling throughout.

---

## Project Structure

```
binance-futures-trading-bot/
  bot/
    __init__.py
    client.py          # Binance API wrapper (direct REST, HMAC-SHA256 signing)
    orders.py          # Order placement logic (MARKET + LIMIT)
    validators.py      # Input validation before any API call
    logging_config.py  # Centralized logging setup
  cli.py               # CLI entry point (argparse)
  requirements.txt     # Dependencies
  trading_bot.log      # Sample log output (MARKET + LIMIT orders)
  trading_bot_demo.ipynb  # Google Colab notebook (run top to bottom)
  README.md
```

---

## Setup Steps

### 1. Clone the repository
```bash
git clone https://github.com/parthsharmaww-ai/binance-futures-trading-bot.git
cd binance-futures-trading-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API keys
Open `cli.py` and replace:
```python
API_KEY    = "your_api_key_here"
API_SECRET = "your_api_secret_here"
```

---

## How to Run

### Place a MARKET order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
```

### Place a LIMIT order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 70000
```

### All available arguments

| Argument  | Required   | Description       | Example         |
|-----------|------------|-------------------|-----------------|
| --symbol  | Yes        | Trading pair      | BTCUSDT         |
| --side    | Yes        | Order side        | BUY or SELL     |
| --type    | Yes        | Order type        | MARKET or LIMIT |
| --qty     | Yes        | Order quantity    | 0.01            |
| --price   | LIMIT only | Limit price       | 70000           |

---

## Run in Google Colab

Open `trading_bot_demo.ipynb` directly in Google Colab and run cells top to bottom. No local setup needed.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/parthsharmaww-ai/binance-futures-trading-bot/blob/main/trading_bot_demo.ipynb)

---

## Example Output

### MARKET order
```
================================================
  📤 ORDER REQUEST SUMMARY
================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
================================================

================================================
  ✅ ORDER SUCCESS
================================================
  Order ID     : 583291
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 67432.10
================================================
```

### LIMIT order
```
================================================
  📤 ORDER REQUEST SUMMARY
================================================
  Symbol     : BTCUSDT
  Side       : SELL
  Type       : LIMIT
  Quantity   : 0.01
  Price      : 70000.0
================================================

================================================
  ✅ ORDER SUCCESS
================================================
  Order ID     : 729104
  Symbol       : BTCUSDT
  Side         : SELL
  Type         : LIMIT
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 67432.10
================================================
```

---

## Logging

All API requests, responses, and errors are logged to `trading_bot.log` with timestamps. Example:

```
2026-05-20 12:00:01 | INFO     | bot.client           | BinanceClient initialised
2026-05-20 12:00:01 | INFO     | bot.orders           | ORDER REQUEST | BTCUSDT | BUY | MARKET | qty=0.01
2026-05-20 12:00:01 | INFO     | bot.orders           | ORDER RESPONSE | orderId=583291 | status=FILLED | executedQty=0.01 | avgPrice=67432.10
2026-05-20 12:00:02 | INFO     | bot.orders           | ORDER REQUEST | BTCUSDT | SELL | LIMIT | qty=0.01 | price=70000.0
2026-05-20 12:00:02 | INFO     | bot.orders           | ORDER RESPONSE | orderId=729104 | status=FILLED | executedQty=0.01 | avgPrice=67432.10
```

---

## Assumptions

- **Mock server**: Bot is tested against a local Flask mock server due to Binance Futures Testnet (testnet.binancefuture.com) being geo-restricted in India. The mock server simulates real Binance Futures API responses including orderId, status, executedQty and avgPrice fields.

- **Switching to real testnet**: Change BASE_URL in bot/client.py and bot/orders.py to https://testnet.binancefuture.com and update API keys from the Futures Testnet dashboard.

- **Symbol format**: Only USDT-M pairs are supported (symbol must end with USDT e.g. BTCUSDT, ETHUSDT).

- **LIMIT orders**: Always placed with timeInForce=GTC (Good Till Cancelled).

---

## Tech Stack

- Python 3.x
- requests — direct REST API calls
- argparse — CLI interface
- flask — local mock server for testing
- hmac + hashlib — HMAC-SHA256 request signing
- logging — structured file and console logging
