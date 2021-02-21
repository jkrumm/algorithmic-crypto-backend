import logging.config
from os import environ

from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .config import config as app_config

celery = Celery(__name__)

CELERY_TASK_LIST = [
    'core.tasks.test',
    'core.tasks.signal',
    'allocate.tasks.allocate',
    'trade.tasks.trade'
]


def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])
    # app.secret_key = app_config.BaseConfig.SECRET_KEY

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    # celery = Celery(include=CELERY_TASK_LIST)
    celery.config_from_object(app.config, force=True)
    # celery is not able to pick result_backend and hence using update
    celery.conf.update(result_backend=app.config['RESULT_BACKEND'])

    from app.public.views import public as public_blueprint
    app.register_blueprint(public_blueprint)

    from app.core.views import core as core_blueprint
    app.register_blueprint(
        core_blueprint,
        url_prefix='/api/v1/core'
    )
    from app.allocate.views import allocate as allocate_blueprint
    app.register_blueprint(
        allocate_blueprint,
        url_prefix='/api/v1/allocate'
    )
    from app.trade.views import trade as trade_blueprint
    app.register_blueprint(
        trade_blueprint,
        url_prefix='/api/v1/trade'
    )

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
