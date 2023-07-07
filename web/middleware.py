from flask import request
from repository.user import User
from utils.helper import FlaskSession


class AuthenticationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'user' in request.cookies:
            token = request.cookies.get('authentication')
            user_id = FlaskSession().get_user_id(token)
            if user_id is not None:
                user = User.query.filter(User.id == int(user_id)).first()
                request.user = user
            else:
                request.user = None
        return self.app(environ, start_response)
