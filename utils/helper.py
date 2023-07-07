import os
import string
import random
import uuid

from logger import logger
from repository.redis_mangement import RedisSession


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


class FlaskSession:
    def __init__(self):
        self.repo = RedisSession()

    def create_token(self, user_id):
        token = uuid.uuid4().hex
        self.repo.set(token, user_id)
        return token

    def get_user_id(self, token):
        user_id = self.repo.get(token)
        return user_id

    def revoke_token(self, token):
        self.repo.delete(token)
        return None
