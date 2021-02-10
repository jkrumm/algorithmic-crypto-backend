import json
from flask import Blueprint, current_app, request
from werkzeug.local import LocalProxy

from app.utils import telegram_bot
from authentication import require_appkey
from app.config import secrets

from app.trade.tasks import trade_btc_eth_task

trade = Blueprint('trade', __name__)
logger = LocalProxy(lambda: current_app.logger)


@trade.before_request
def before_request_func():
    current_app.logger.name = 'allocate'


@trade.route('/run', methods=['POST'])
def run():
    content = request.get_json()
    logger.info('trade allocate route hit: ' + json.dumps(content))
    telegram_bot("🟢 TRADE", "GET /trade endpoint: " + json.dumps(content))
    if 'USD' not in content or 'BTC' not in content or 'ETH' not in content:
        telegram_bot("🟠 TRADE", "INVALID BODY!")
        return "Invalid body"
    if content == {'USD': 0, 'BTC': 0, 'ETH': 0}:
        telegram_bot("🟠 TRADE", "No changes!")
        return "No changes!"
    for user in secrets:
        trade_btc_eth_task.apply_async(args=[user, content])
    return 'Trade started!'


@trade.route('/test', methods=['GET'])
def test():
    logger.info('trade test route hit')
    telegram_bot("TEST", "GET /test endpoint trade")
    return 'Congratulations! Your trade-app test route is running!'


@trade.route('/restricted', methods=['GET'])
@require_appkey
def restricted():
    return 'Congratulations! Your trade-app restricted route is running via your API key!'
