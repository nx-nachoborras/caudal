from telegram_client import TelegramClient
from saih import SAIHClient

if __name__ == '__main__':
    saih_client = SAIHClient()
    saih_response = saih_client.get_carraixet_flow()

    if saih_response:
        telegram_client = TelegramClient()
        telegram_client.send_message(saih_response)