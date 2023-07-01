import os
from logger import logger


def mkdir(directory: str):
    try:
        os.mkdir(directory)
    except OSError as e:
        logger.error(f'OSError -- {e}')


def is_exist_path(directory: str):
    try:
        return os.path.exists(directory)
    except OSError as e:
        logger.error(f'OSError -- {e}')
