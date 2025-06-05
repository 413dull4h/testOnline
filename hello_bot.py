import time
import requests

# --- Telegram Bot Info ---
BOT_TOKEN = "8107336942:AAHEjY6v6-pVJSS086n2e3hrAfj3ktQ_iq8"
CHAT_ID = "1339318363"

# --- Binance Trading Pairs ---
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT",
    "AVAXUSDT", "PEPEUSDT", "SUIUSDT", "LTCUSDT", "BNBUSDT",
    "TRUMPUSDT", "BONKUSDT"
]

# --- Send Message to Telegram ---
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Sent:\n", text)
        else:
            print("⚠️ Telegram Error:", response.text)
    except Exception as e:
        print("Telegram Exception:", e)

# --- Fetch price from Binance API ---
def fetch_price(symbol):
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url, params={"symbol": symbol})
        data = response.json()
        if "price" in data:
            return float(data["price"])
        else:
            print(f"⚠️ Unexpected response for {symbol}:", data)
            return None
    except Exception as e:
        print(f"Error fetching {symbol}:", e)
        return None

# --- Main Loop ---
if __name__ == "__main__":
    while True:
        prices = []
        for symbol in SYMBOLS:
            price = fetch_price(symbol)
            if price is not None:
                prices.append(f"{symbol}: ${price:,.6f}")
        if prices:
            message = "📊 Binance Prices:\n" + "\n".join(prices)
            send_message(message)
        else:
            print("⚠️ No prices fetched.")
        time.sleep(30)
