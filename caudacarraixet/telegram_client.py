import logging
import os
from textwrap import dedent

import requests


class TelegramClient:

    def __init__(self):
        self.token = os.environ.get('TELEGRAM_TOKEN')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("SAIH Client initialized")

    def send_message(self, text):

        message = self._prepare_message(text)

        self.logger.info(f"Sending message: {message}")
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}"
        response = requests.request("GET", url)

        if response.json()['ok'] is False:
            self.logger.error(f"Error {response.status_code}")
            self.logger.error(f"Error {response.text}")
            return None
        self.logger.info(response.json()['result'])
        return response.json()['result']

    @staticmethod
    def _prepare_message(data):
        description = data['description']
        dimension = data['dimension']
        current_flow_value = data['current_flow_value']
        current_flow_time = data['current_flow_time']
        flow_trend = data['flow_trend']
        max_carraixet_flow = data['max_carraixet_flow']

        message = f"""
        {description} ({dimension})
        Valor actual: {current_flow_value} m3/s
        Última actualización (Horas en UTC): {current_flow_time}
        Tendencia: {flow_trend}
        Límite máximo: {max_carraixet_flow} m3/s
        Aviso especial: {data['warning'] or "No hay avisos especiales"}
        """

        return dedent(message)


if __name__ == '__main__':
    text = "Hello, world!"
    telegram_client = TelegramClient()
    telegram_client.send_message(text)
