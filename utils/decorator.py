from functools import wraps
from flask import g

from logger import logger
from use_case.auth import GetUser
from utils.exceptions import AuthenticationRequired


def authentication(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            if g.user_id is None:
                raise AuthenticationRequired("User should be logged in...")
            has_err, res = GetUser(user_id=g.user_id).run()
            if not has_err:
                g.current_user = res
                return func(*args, **kwargs)
            raise AuthenticationRequired("User should be logged in...")
        except Exception as e:
            logger.error(e)
            raise AuthenticationRequired("User should be logged in...")
    return decorated
