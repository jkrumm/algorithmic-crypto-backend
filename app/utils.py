import requests
from pandas import DataFrame
from flask import current_app
from werkzeug.local import LocalProxy
from app.config import BaseConfig

from app import celery

logger = LocalProxy(lambda: current_app.logger)


class BaseTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        logger.info(exc)
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        logger.info(exc)
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


def backoff(attempts):
    """Return a backoff delay, in seconds, given a number of attempts.
    The delay increases very rapidly with the number of attemps:
    1, 2, 4, 8, 16, 32, ...
    """
    return 3 ** attempts


def telegram_bot(task, msg):
    logger.info('running telegram_bot util : ' + task + " | " + msg)
    requests.get(
        'https://api.telegram.org/bot' + BaseConfig.BOT_TELEGRAM_TOKEN \
        + '/sendMessage?chat_id=' + BaseConfig.BOT_TELEGRAM_ID \
        + '&parse_mode=html&text=' + "<b>" + task + "</b>   <i>" + msg + "</i>")


def get_df(cursor):
    try:
        return DataFrame(list(cursor))
    except Exception as exc:
        logger.info(exc)


def transform_cursor_dict(obj):
    if '_id' in obj: del obj['_id']
    return obj
