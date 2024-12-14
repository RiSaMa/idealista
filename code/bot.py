import requests
import os

verify = True # in macos locally, I might have to use False or resolve the issue

def get_bot_token():
    return os.getenv('TELEGRAM_TOKEN')

def get_chat_ids():
    return [
        "451966009", # Ricardo
        "1602683666", # Eliska
        ]

def send_telegram_message(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=payload, verify=verify)

    if response.status_code == 200:
        print("Telegram message sent successfully.")
        return
    else:
        print("Failed to send Telegram message.")
        print(f"Error: {response.status_code} - {response.text}")
        return

def send_telegram_messages(message):
    bot_token = get_bot_token()
    for chat_id in get_chat_ids():
        send_telegram_message(message, bot_token, chat_id)
        