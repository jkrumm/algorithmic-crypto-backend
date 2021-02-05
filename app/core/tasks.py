import requests
from datetime import datetime
from celery.utils.log import get_task_logger

from app.config import BaseConfig, kraken, get_db
from app import celery

logger = get_task_logger(__name__)

db = get_db()['dev']


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
    return 2 ** attempts


@celery.task(base=BaseTask, name='core.tasks.test',
             soft_time_limit=60, time_limit=65)
def test_task():
    logger.info('running test task')
    return True


@celery.task(bind=True, base=BaseTask, name='core.tasks.telegram_bot',
             soft_time_limit=3, time_limit=5, max_retries=2)
def telegram_bot_task(self, task, msg):
    logger.info('running telegram_bot task : ' + task + " | " + msg)
    full_msg = "<b>" + task + "</b> | <i>" + msg + "</i>"
    try:
        requests.get(
            'https://api.telegram.org/bot' + BaseConfig.BOT_TELEGRAM_TOKEN \
            + '/sendMessage?chat_id=' + BaseConfig.BOT_TELEGRAM_ID \
            + '&parse_mode=html&text=' + full_msg)
    except Exception as exc:
        logger.info(exc)
        self.retry(countdown=backoff(self.request.retries), exc=exc)
    return True


@celery.task(bind=True, base=BaseTask, name='core.tasks.signal',
             soft_time_limit=20, time_limit=30, max_retries=2)
def signal_task(self, ticker, interval, action, source):
    logger.info('running signal task')
    try:
        ticker = ticker.replace('XBT', 'BTC')
        db.signal.insert_one({
            "action": action,
            "ticker": ticker,
            "interval": interval,
            "time": datetime.now(),
            "price": kraken.fetch_ticker(ticker)['close'],
            "source": source
        })
    except Exception as exc:
        logger.info(exc)
        telegram_bot_task.apply_async(
            args=["🔴 SIGNAL",
                  "FAILED inserting signal : " + ticker + " | " + action])
        telegram_bot_task.apply_async(args=["🔴 EXCEPTION", str(exc)])
        self.retry(countdown=backoff(self.request.retries), exc=exc)
    telegram_bot_task.apply_async(
        args=["🟢 SIGNAL",
              "Successfully inserted signal : " + ticker + " | " + action])
    return True
