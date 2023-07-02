import os
import string
import random
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


def join_path(base_path: str, sub_path: str):
    try:
        return os.path.join(base_path, sub_path)
    except OSError as e:
        logger.error(f'OSError -- {e}')


def splitext(file_name: str):
    try:
        return os.path.splitext(file_name)
    except OSError as e:
        logger.error(f'OSError -- {e}')


def generate_random_characters(length=13):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))
