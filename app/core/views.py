from flask import Blueprint, current_app, request
from werkzeug.local import LocalProxy

from app.utils import telegram_bot, backoff
from authentication import require_appkey
from app.config import BaseConfig

from app.core.tasks import test_task, signal_task

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = 'core'


@core.route('/signal', methods=['POST'])
def signal():
    content = request.get_json()
    logger.info('core signal route hit')
    telegram_bot("🟢 SIGNAL", "GET /signal endpoint")
    if 'interval' not in content or 'ticker' not in content \
        or 'source' not in content or 'secret' not in content \
        or 'alt' not in content:
        telegram_bot("🟠 SIGNAL", "INVALID BODY!")
        return "Invalid body"
    if content['secret'] != BaseConfig.TV_KEY:
        telegram_bot("🟠 SIGNAL", "WRONG SECRET!")
        return "Unauthorized"
    if content['action'] != "buy" and content['action'] != "sell":
        telegram_bot("🟠 SIGNAL", "NO VALID ACTION! Only buy or sell accepted!")
        return "No valid action : " + content['action']
    try:
        signal_task.apply_async(args=[content['ticker'], content['interval'],
                                      content['alt'], content['source'],
                                      content['action']])
    except Exception as exc:
        print(exc)
        telegram_bot("🔴 SIGNAL",
                     "GET /signal endpoint | failed starting signal_task")
        telegram_bot("🔴 EXCEPTION", str(exc))
        return str(exc)
    return 'Received Signal!'


@core.route('/test', methods=['GET'])
def test():
    test_task.delay()
    logger.info('core test route hit')
    telegram_bot("🟢 TEST", "GET /test endpoint core")
    return 'Congratulations! Your core-app test route is running!'


@core.route('/restricted', methods=['GET'])
@require_appkey
def restricted():
    return 'Congratulations! Your core-app restricted route is running via your API key!'
