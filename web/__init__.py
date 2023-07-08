import os.path

from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import settings
# from web.middleware import AuthenticationMiddleware

db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
template_dir = os.path.abspath('templates/')
static_dir = os.path.abspath('templates/static/')

from celery import Celery, Task


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery('flask-celery-app', task_cls=FlaskTask,
                        broker_url=settings.CELERY_BROKER_URL,
                        result_backend=settings.CELERY_RESULT_BACKEND,
                        broker_connection_timeout=settings.BROKER_CONNECTION_TIMEOUT,
                        broker_connection_retry=settings.BROKER_CONNECTION_RETRY,
                        broker_connection_retry_on_startup=settings.BROKER_CONNECTION_RETRY_ON_STARTUP,
                        broker_connection_max_retries=settings.BROKER_CONNECTION_MAX_RETRIES,
                        )
    # celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app() -> Flask:
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_mapping(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///../app.db',
        SQLALCHEMY_ECHO=True,
    )

    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    app.config.from_prefixed_env()
    celery_init_app(app)
    app.static_url_path = static_dir
    # app.wsgi_app = AuthenticationMiddleware(app.wsgi_app)

    from web.auth import auth_bp
    from web.player import movie_bp
    from web.panel import panel_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(panel_bp)

    return app


def create_test_app():
    app = Flask(__name__, template_folder=template_dir)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test_app.db'
    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    # app.wsgi_app = AuthenticationMiddleware(app.wsgi_app)
    return app
