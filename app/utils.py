from functools import wraps
import requests
import json
from pandas import DataFrame
from flask import current_app, session, redirect
from werkzeug.local import LocalProxy
from cryptography.fernet import Fernet
from app.config import BaseConfig

import http.client

from app import celery

logger = LocalProxy(lambda: current_app.logger)

cipher_suite = Fernet(BaseConfig.FERNET_KEY)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


def encrypt(secret):
    return cipher_suite.encrypt(secret.encode()).decode()


def decrypt(token):
    return cipher_suite.decrypt(token.encode()).decode()


def change_user_app_metadata(user_id, app_metadata):
    conn = http.client.HTTPSConnection(BaseConfig.AUTH0_DOMAIN)
    payload = json.dumps({
        "app_metadata": app_metadata
    })
    headers = {
        'authorization': BaseConfig.AUTH0_CLIENT_SECRET,
        'content-type': "application/json"
    }

    conn.request("PATCH", "/api/v2/users/" + user_id, payload, headers)

    res = conn.getresponse()
    data = res.read()
    logger.info(data.decode("utf-8"))


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
        'https://api.telegram.org/bot' + BaseConfig.BOT_TELEGRAM_TOKEN
        + '/sendMessage?chat_id=' + BaseConfig.BOT_TELEGRAM_ID
        + '&parse_mode=html&text=' + "<b>" + task + " | "
        + BaseConfig.APPLICATION_ENV + "</b>\n<i>" + msg + "</i>")


def get_df(cursor):
    try:
        return DataFrame(list(cursor))
    except Exception as exc:
        logger.info(exc)


def transform_cursor_dict(obj):
    if '_id' in obj: del obj['_id']
    return obj
