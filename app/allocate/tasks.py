import json
import pandas as pd
from datetime import datetime
from celery.utils.log import get_task_logger

from app.utils import BaseTask, backoff, telegram_bot
from app.config import get_db, BaseConfig, kraken, secrets
from app.trade.tasks import trade_btc_eth_task
from app import celery

logger = get_task_logger(__name__)

db = get_db()[BaseConfig.DB]


@celery.task(bind=True, base=BaseTask, name='allocate.tasks.allocate',
             soft_time_limit=100, time_limit=150, max_retries=2)
def allocate_btc_eth_task(self):
    logger.info('running allocate')
    changes = {"USD": 0, "BTC": 0, "ETH": 0}
    try:
        s_db = pd.DataFrame(list(db.signal.find({}))) \
            .sort_values(by='time', ascending=False).reset_index(drop=True)

        s = {"ETH/BTC": 0, "BTC/USD": 0, "ETH/USD": 0}
        for index, row in s_db.iterrows():
            if row['ticker'] == "ETH/BTC" and s["ETH/BTC"] == 0:
                logger.info("HERE : " + row['action'])
                s["ETH/BTC"] = "buy" if row['action'] == "buy" else "sell"
            elif row['ticker'] == "BTC/USD" and s["BTC/USD"] == 0:
                s["BTC/USD"] = "buy" if row['action'] == "buy" else "sell"
            elif row['ticker'] == "ETH/USD" and s["ETH/USD"] == 0:
                s["ETH/USD"] = "buy" if row['action'] == "buy" else "sell"

        a = {"USD": 0, "BTC": 0, "ETH": 0,
             "btc_price": kraken.fetch_ticker("BTC/USD")['close'],
             "eth_price": kraken.fetch_ticker("ETH/USD")['close'],
             "eth_btc_price": kraken.fetch_ticker("ETH/BTC")['close'],
             "time": datetime.now()}
        if s["ETH/BTC"] == "buy" and s["ETH/USD"] == "buy":
            a["ETH"] = 100
        elif s["BTC/USD"] == "buy":
            a["BTC"] = 100
        else:
            a["USD"] = 100

        c_a = pd.DataFrame(list(db.allocation_btc_eth.find({}))) \
            .sort_values(by='time', ascending=False).reset_index(drop=True)

        changes = {
            "USD": a["USD"] - c_a.iloc[0]["USD"],
            "BTC": a["BTC"] - c_a.iloc[0]["BTC"],
            "ETH": a["ETH"] - c_a.iloc[0]["ETH"]
        }

        if changes["USD"] == 0 and changes["BTC"] == 0 and changes["ETH"] == 0:
            telegram_bot("🟢 ALLOCATE", "No changes")
            return True
        elif changes["USD"] == 100 and changes["BTC"] == -100:
            telegram_bot("🟢 ALLOCATE", "Sell BTC to USD")
        elif changes["USD"] == 100 and changes["ETH"] == -100:
            telegram_bot("🟢 ALLOCATE", "Sell ETH to USD")
        elif changes["BTC"] == 100 and changes["ETH"] == -100:
            telegram_bot("🟢 ALLOCATE", "Sell ETH to BTC")
        elif changes["ETH"] == 100 and changes["BTC"] == -100:
            telegram_bot("🟢 ALLOCATE", "Sell BTC to ETH")
        elif changes["USD"] == -100 and changes["BTC"] == 100:
            telegram_bot("🟢 ALLOCATE", "Buy BTC with USD")
        elif changes["USD"] == -100 and changes["ETH"] == 100:
            telegram_bot("🟢 ALLOCATE", "Buy ETH with USD")
        else:
            telegram_bot("🔴 ALLOCATE", "Invalid allocation result!")
            telegram_bot("🔴 EXCEPTION", json.dumps(changes))
            return False

        db.allocation_btc_eth.insert_one(a)

    except Exception as exc:
        logger.info(exc)
        telegram_bot("🔴 ALLOCATE",
                     "FAILED running allocate_btc_eth_task task")
        telegram_bot("🔴 EXCEPTION", str(exc))
        self.retry(countdown=backoff(self.request.retries), exc=exc)

    changes = {
        "USD": str(changes['USD']),
        "BTC": str(changes['BTC']),
        "ETH": str(changes['ETH']),
    }

    for user in secrets:
        trade_btc_eth_task.apply_async(
            args=[user, changes])

    telegram_bot("🟢 ALLOCATE", "Successfully allocated btc_eth portfolio")
    telegram_bot("🟢 ALLOCATE", str(a))
    return True
