import pandas as pd
from datetime import datetime
from celery.utils.log import get_task_logger

from app.config import kraken, get_db
from app import celery
from app.utils import BaseTask, backoff, telegram_bot
from app.allocate.tasks import allocate_btc_eth_task

logger = get_task_logger(__name__)

db = get_db()['dev']


@celery.task(base=BaseTask, name='core.tasks.test',
             soft_time_limit=60, time_limit=65)
def test_task():
    logger.info('running test task')
    return True


@celery.task(bind=True, base=BaseTask, name='core.tasks.signal',
             soft_time_limit=20, time_limit=30, max_retries=2)
def signal_task(self, ticker, interval, alt, source, action):
    logger.info('running signal task')
    try:
        ticker = ticker.replace('XBT', 'BTC')
        if action == "unset":
            l_s = pd.DataFrame(
                list(db.signal.find({"ticker": ticker}))).sort_values(
                by='time', ascending=False).reset_index()
            action = "buy" if l_s.iloc[0]['action'] == "sell" else "sell"
        db.signal.insert_one({
            "ticker": ticker,
            "action": action,
            "interval": interval,
            "alt": alt,
            "time": datetime.now(),
            "price": kraken.fetch_ticker(ticker)['close'],
            "stop": kraken.fetch_ticker(ticker)['close'] * 0.93,
            "source": source
        })
    except Exception as exc:
        logger.info(exc)
        telegram_bot("🔴 SIGNAL",
                     "FAILED inserting signal : " + ticker + " | " + action)
        telegram_bot("🔴 EXCEPTION", str(exc))
        self.retry(countdown=backoff(self.request.retries), exc=exc)
    telegram_bot("🟢 SIGNAL",
                 "Successfully inserted signal : " + ticker + " | " + action)
    allocate_btc_eth_task.apply_async()
    return True
