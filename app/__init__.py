import logging.config
import settings
from common.cache import Redis
from flask import Flask, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from route.route import register_route_blueprint
from werkzeug.utils import import_string


def create_app():
    logging.config.dictConfig(import_string("settings.LOGGING_CONFIG"))
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings)
    app.cache = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
    ).get_connection()

    Limiter(app, key_func=get_remote_address, default_limits=["50 per minute"])

    register_route_blueprint(app)

    return app


app = create_app()


@app.route("/health")
def health_check():
    return jsonify({"status": "ok", "cache": current_app.cache.ping()}), 200
