import os

import requests


class TelegramClient:

    def __init__(self):
        self.token = os.environ.get('TELEGRAM_TOKEN')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    def send_message(self, text):

        message = self._prepare_message(text)

        print(f"Sending message: {message}")
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}"
        response = requests.request("GET", url)

        if response.json()['ok'] is False:
            print(f"Error {response.status_code}")
            print(f"Error {response.text}")
            return None
        print(response.json()['result'])
        return response.json()['result']

    def _prepare_message(self, data):
        description = data['description']
        dimension = data['dimension']
        current_flow_value = data['current_flow_value']
        current_flow_time = data['current_flow_time']
        flow_trend = data['flow_trend']
        max_carraixet_flow = data['max_carraixet_flow']

        message = f"{description} ({dimension})\n" \
                  f"Valor actual: {current_flow_value} m3/s\n" \
                  f"Última actualización: {current_flow_time}\n" \
                  f"Tendencia: {flow_trend}\n" \
                  f"Límite máximo: {max_carraixet_flow} m3/s"

        return message


if __name__ == '__main__':
    text = "Hello, world!"
    telegram_client = TelegramClient()
    telegram_client.send_message(text)
