import os

import requests


class TelegramClient:

    def __init__(self):
        self.token = os.environ.get('TELEGRAM_TOKEN')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    def send_message(self, text):

        print(f"Sending message: {text}")
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={text}"
        response = requests.request("GET", url)

        if response.json()['ok'] is False:
            print(f"Error {response.status_code}")
            print(f"Error {response.text}")
            return None
        print(response.json()['result'])
        return response.json()['result']


if __name__ == '__main__':
    text = "Hello, world!"
    telegram_client = TelegramClient()
    telegram_client.send_message(text)
