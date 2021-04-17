import logging
from datetime import datetime


class Logger:
    def info(self, msg):
        dt_string = datetime.now().strftime("%d_%m_%Y")
        logging.basicConfig(filename=f'info_{dt_string}.log', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info(msg)

    def error(self, msg):
        dt_string = datetime.now().strftime("%d_%m_%Y")
        logging.basicConfig(filename=f'error_{dt_string}.log', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.error(msg)
