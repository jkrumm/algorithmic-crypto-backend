import requests
import ccxt
from datetime import datetime
from celery.utils.log import get_task_logger

from tasks import BaseTask, backoff, telegram_bot_task
from app.config import BaseConfig, kraken, get_db
from app import celery

logger = get_task_logger(__name__)

db = get_db()['dev']


@celery.task(bind=True, base=BaseTask, name='core.allocate.allocate',
             soft_time_limit=100, time_limit=150, max_retries=2)
def allocate(self):
    logger.info('running allocate task')
    try:
        return
    except Exception as exc:
        logger.info(exc)
        self.retry(countdown=backoff(self.request.retries), exc=exc)
    return True
