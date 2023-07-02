import os.path

from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
template_dir = os.path.abspath('templates/')
static_dir = os.path.abspath('templates/static')


def create_app():
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_mapping(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///../app.db',
        SQLALCHEMY_ECHO=True,
    )

    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)

    from web.auth import auth_bp
    from web.player import movie_bp
    from web.panel import panel_bp
    from repository.user import User, Permission
    from repository.file import Movie
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
    return app
