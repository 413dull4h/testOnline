# import time
# import requests
#
# # --- Telegram Bot Info ---
# BOT_TOKEN = "8107336942:AAHEjY6v6-pVJSS086n2e3hrAfj3ktQ_iq8"
# CHAT_ID = "1339318363"
#
# # --- Binance Trading Pairs ---
# SYMBOLS = [
#     "BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT",
#     "AVAXUSDT", "PEPEUSDT", "SUIUSDT", "LTCUSDT", "BNBUSDT",
#     "TRUMPUSDT", "BONKUSDT"
# ]
#
# # --- Send Message to Telegram ---
# def send_message(text):
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
#     payload = {"chat_id": CHAT_ID, "text": text}
#     try:
#         response = requests.post(url, data=payload)
#         if response.status_code == 200:
#             print("✅ Sent:\n", text)
#         else:
#             print("⚠️ Telegram Error:", response.text)
#     except Exception as e:
#         print("Telegram Exception:", e)
#
# # --- Fetch price from Binance API ---
# def fetch_price(symbol):
#     url = "https://api.binance.com/api/v3/ticker/price"
#     try:
#         response = requests.get(url, params={"symbol": symbol})
#         data = response.json()
#         if "price" in data:
#             return float(data["price"])
#         else:
#             print(f"⚠️ Unexpected response for {symbol}:", data)
#             return None
#     except Exception as e:
#         print(f"Error fetching {symbol}:", e)
#         return None
#
# # --- Main Loop ---
# if __name__ == "__main__":
#     while True:
#         prices = []
#         for symbol in SYMBOLS:
#             price = fetch_price(symbol)
#             if price is not None:
#                 prices.append(f"{symbol}: ${price:,.6f}")
#         if prices:
#             message = "📊 Binance Prices:\n" + "\n".join(prices)
#             send_message(message)
#         else:
#             print("⚠️ No prices fetched.")
#         time.sleep(30)

import time
import threading
import requests
from flask import Flask

# --- Telegram Bot Info ---
BOT_TOKEN = "8107336942:AAHEjY6v6-pVJSS086n2e3hrAfj3ktQ_iq8"
CHAT_ID = "1339318363"

# --- Binance Symbols to Track ---
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT",
    "ADAUSDT", "AVAXUSDT", "PEPEUSDT", "SUIUSDT",
    "LTCUSDT", "BNBUSDT", "TRUMPUSDT", "BONKUSDT"
]

# --- Send Message to Telegram ---
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("Telegram API Error:", response.text)
        else:
            print("✅ Sent:", text)
    except Exception as e:
        print("Telegram Error:", e)

# --- Get Binance Price for a Symbol ---
def fetch_price(symbol):
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        res = requests.get(url, params={"symbol": symbol})
        data = res.json()
        return float(data["price"]) if "price" in data else None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

# --- Bot Loop ---
def run_bot():
    while True:
        prices = []
        for symbol in SYMBOLS:
            price = fetch_price(symbol)
            if price is not None:
                prices.append(f"{symbol}: ${price:,.6f}")
            else:
                prices.append(f"{symbol}: ❌ Unavailable")
        if prices:
            text = "📊 Binance Prices:\n" + "\n".join(prices)
            send_message(text)
        else:
            print("⚠️ No prices fetched.")
        time.sleep(30)

# --- Flask Web Server ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Crypto Price Bot (Binance) is running!"

# --- Run Bot Thread and Web Server ---
threading.Thread(target=run_bot).start()
app.run(host="0.0.0.0", port=8080)
