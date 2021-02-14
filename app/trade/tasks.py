import json
import ccxt
import pandas as pd
from datetime import datetime
from celery.utils.log import get_task_logger

from app.utils import BaseTask, backoff, telegram_bot
from app.config import get_db
from app import celery

logger = get_task_logger(__name__)

db = get_db()


@celery.task(bind=True, base=BaseTask, name='trade.tasks.trade',
             soft_time_limit=100, time_limit=150, max_retries=2)
def trade_btc_eth_task(self, user, changes):
    logger.info('running trade btc_eth for ' + user['name'])
    try:
        changes = {
            "USD": int(changes['USD']),
            "BTC": int(changes['BTC']),
            "ETH": int(changes['ETH'])
        }

        kraken = ccxt.kraken({
            'apiKey': user['key'],
            'secret': user['secret'],
            'enableRateLimit': True,
            "timeout": 100000,
            # 'verbose': True,
            'options': {
                'fetchMinOrderAmounts': False
            }
        })

        kraken.check_required_credentials()
        kraken.load_markets()
        balance_usd = update_balance_usd(kraken)
        balance_btc = update_balance_btc(kraken)
        balance_eth = update_balance_eth(kraken)

        output = {}

        telegram_bot("🟢 TRADE", json.dumps(changes))
        telegram_bot("🟢 TRADE", "Current balance for " + user['name']
                     + " | USD: " + str(balance_usd) + " | BTC: "
                     + str(balance_btc) + " | ETH: " + str(balance_eth))

        if balance_btc > 0:
            output['sell_order_btc'] = kraken.create_order(
                'BTC/USD', 'market', 'sell', balance_btc)['info']['descr'][
                'order']
            telegram_bot("🟢 TRADE", "Sold BTC: " + output['sell_order_btc'])

        if balance_eth > 0:
            output['sell_order_eth'] = kraken.create_order(
                'ETH/USD', 'market', 'sell', balance_eth)['info']['descr'][
                'order']
            telegram_bot("🟢 TRADE", "Sold ETH: " + output['sell_order_eth'])

        balance_usd = update_balance_usd(kraken)
        btc_price = kraken.fetch_ticker('BTC/USD')['close']
        eth_price = kraken.fetch_ticker('ETH/USD')['close']

        if balance_usd > 0 and changes["BTC"] == 100:
            output['buy_order_btc'] = kraken.create_order(
                'BTC/USD', 'market', 'buy', (balance_usd / btc_price) * 0.97)[
                'info']['descr']['order']
            telegram_bot("🟢 TRADE", "Buy BTC: " + output['buy_order_btc'])

        if balance_usd > 0 and changes["ETH"] == 100:
            output['buy_order_eth'] = kraken.create_order(
                'ETH/USD', 'market', 'buy', (balance_usd / eth_price) * 0.97)[
                'info']['descr']['order']
            telegram_bot("🟢 TRADE", "Buy ETH: " + output['buy_order_eth'])

        balance_usd = update_balance_usd(kraken)
        balance_btc = update_balance_btc(kraken)
        balance_eth = update_balance_eth(kraken)

        telegram_bot("🟢 TRADE", "Balance for " + user['name']
                     + " | USD: " + str(balance_usd) + " | BTC: "
                     + str(balance_btc) + " | ETH: " + str(balance_eth))

        if output == {}:
            telegram_bot("🟠 TRADE", "No trades for: " + user['name'])

    except Exception as exc:
        logger.info(exc)
        telegram_bot("🔴 TRADE",
                     "FAILED running trade_btc_eth_task task for "
                     + user['name'])
        telegram_bot("🔴 EXCEPTION", str(exc))
        self.retry(countdown=backoff(self.request.retries), exc=exc)

    telegram_bot("🟢 TRADE",
                 "Successfully executed btc_eth trades for " + user['name'])
    return True


def update_balance_usd(kraken):
    return float(kraken.fetch_balance()["info"]['ZUSD'])


def update_balance_btc(kraken):
    return float(kraken.fetch_balance()["info"]['XXBT'])


def update_balance_eth(kraken):
    return float(kraken.fetch_balance()["info"]['XETH'])
