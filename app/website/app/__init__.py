import os

from flask import (
    Flask,
    g
)

from flask_restful import Api

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Base

from app.routes import route
from app.config import config, init_config

def create_flask_app():
    app = Flask(__name__)
    api = Api(app)

    route(api)

    path = os.environ.get('CONFIG_PATH') if os.environ.get(
        'CONFIG_PATH') else "./settings.ini"
    init_config(path)

    engine = create_engine(config["SQLALCHEMY"]["SQLALCHEMY_DATABASE_URI"], pool_size=10, max_overflow=20)
    Base.metadata.bind = engine

    @app.before_request
    def before_request():
        g.db = Session(engine)

    try:
        app.config.update(dict(
            SECRET_KEY=str(config['FLASK_APP']['FLASK_APP_SECRET_KEY'])
        ))
        print(f"\n\033[32m Сервер запустился с конфигом:\n\033[32m {path}\n")
    except KeyError:
        print(f"\033[31m Файл {path} не найден или неверный")

    return app