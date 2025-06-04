import time
import requests

BOT_TOKEN = "8107336942:AAHEjY6v6-pVJSS086n2e3hrAfj3ktQ_iq8"
CHAT_ID = "1339318363"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=payload)
        print("Sent:", text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        send_message("👋 Hello from Python!")
        time.sleep(10)