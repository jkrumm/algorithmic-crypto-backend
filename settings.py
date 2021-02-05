"""Settings file will be here, please do not
create another settings file, you better dynamicaly
update the value using environtment variable
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

APP_KEY = os.getenv("APP_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRY = int(os.getenv("TOKEN_EXPIRY"))

TIMEZONE = "UTC"

STATSD_HOST = os.environ.get("STATSD_HOST", "localhost")
STATSD_PORT = os.environ.get("STATSD_PORT", 8125)
STATSD_PREFIX = os.environ.get("STATSD_PREFIX", "flask.rq")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT", 3306)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "flask_rq")

REDIS_URL = os.environ.get("REDIS_URL")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 0)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

NSQD_URL = os.environ.get("NSQD_URL")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(process)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json_formatter": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)d %(threadName)s "
            "%(name)s %(levelname)s %(pathname)s %(lineno)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "json_formatter",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": "logs/debug.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "flask.app": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["file_handler", "wsgi", "console"],
        }
    },
    "root": {"level": "ERROR", "handlers": ["wsgi", "console"], "propagate": False},
}
