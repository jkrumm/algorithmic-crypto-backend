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
    'allocate.tasks.get_signals',
    'allocate.tasks.allocate_signals',
    'allocate.tasks.get_allocation',
    'allocate.tasks.change_allocation',
    'allocate.tasks.post_allocation'
]


def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    # celery = Celery(include=CELERY_TASK_LIST)
    celery.config_from_object(app.config, force=True)
    # celery is not able to pick result_backend and hence using update
    celery.conf.update(result_backend=app.config['RESULT_BACKEND'])

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

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
