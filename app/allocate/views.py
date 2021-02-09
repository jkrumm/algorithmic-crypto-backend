from flask import Blueprint, current_app
from werkzeug.local import LocalProxy

from app.utils import telegram_bot
from authentication import require_appkey

from app.allocate.tasks import allocate_btc_eth_task

allocate = Blueprint('allocate', __name__)
logger = LocalProxy(lambda: current_app.logger)


@allocate.before_request
def before_request_func():
    current_app.logger.name = 'allocate'


@allocate.route('/run', methods=['GET'])
def run():
    logger.info('allocate allocate route hit')
    telegram_bot("🟢 ALLOCATE", "GET /allocate endpoint")
    allocate_btc_eth_task.apply_async()
    return 'Allocation started!'


@allocate.route('/test', methods=['GET'])
def test():
    logger.info('allocate test route hit')
    telegram_bot("TEST", "GET /test endpoint allocate")
    return 'Congratulations! Your core-app test route is running!'


@allocate.route('/restricted', methods=['GET'])
@require_appkey
def restricted():
    return 'Congratulations! Your allocate-app restricted route is running via your API key!'
