import logging

from telegram_client import TelegramClient
from saih import SAIHClient

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s',
                        level=logging.DEBUG,
                        filename="/Users/nacho.borras/Documents/caudacarraixet.log",
                        filemode="a")

    saih_client = SAIHClient()
    saih_response = saih_client.get_carraixet_flow()

    logger = logging.getLogger(__name__)


    if saih_response.get("warning"):
    # if True:
        telegram_client = TelegramClient()
        telegram_client.send_message(saih_response)
    else:
        logger.info("No warning message to send")