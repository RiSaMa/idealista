import requests

def get_bot_token():
    return "7851996033:AAFPgP9udSDFCUGBOJQGo_DtkD--cy8QO1w"

def get_chat_id():
    return "451966009"

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=payload, verify=False)

    if response.status_code == 200:
        print("Telegram message sent successfully.")
        return
    else:
        print("Failed to send Telegram message.")
        print(f"Error: {response.status_code} - {response.text}")
        return