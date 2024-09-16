import os
import logging
from logging.handlers import RotatingFileHandler

def logger_settings(log_file="./log/debug.log"):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    p_dir = os.path.dirname(log_file)
    os.makedirs(p_dir, exist_ok=True)

    file_handler = RotatingFileHandler(log_file, maxBytes=200*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s | %(name)s: | %(lineno)s | %(funcName)s | %(pathname)s | [%(levelname)s]: %(message)s')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.debug("Application Starts")

    return logger


if __name__ == "__main__":
    logger = logger_settings()
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")