import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Set logging level to INFO for production
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='logs/app.log',  # Log to a file named app.log
        filemode='a'
    )


setup_logging()
logger = logging.getLogger(__name__)
