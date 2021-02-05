from flask import Blueprint, current_app, request, jsonify
from werkzeug.local import LocalProxy

from authentication import require_appkey
from app.config import BaseConfig

from .tasks import test_task, telegram_bot_task, signal_task

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = 'core'


@core.route('/test', methods=['GET'])
def test():
    logger.info('app test route hit')
    telegram_bot_task.delay("TEST", "GET /test endpoint")
    test_task.delay()
    return 'Congratulations! Your core-app test route is running!'


@core.route('/signal', methods=['POST'])
def signal():
    content = request.get_json()
    logger.info('app signal route hit')
    telegram_bot_task.apply_async(args=["🟢 SIGNAL", "GET /signal endpoint"])
    if 'interval' not in content or 'ticker' not in content \
        or 'source' not in content or 'secret' not in content \
        or 'action' not in content:
        telegram_bot_task.apply_async(args=["🟠 SIGNAL", "INVALID BODY!"])
        return "Invalid body"
    if content['secret'] != BaseConfig.TV_KEY:
        telegram_bot_task.apply_async(args=["🟠 SIGNAL", "WRONG SECRET!"])
        return "Unauthorized"
    if content['action'] != "buy" and content['action'] != "sell":
        telegram_bot_task.apply_async(args=["🟠 SIGNAL", "NO ACTION!"])
        return "No valid action : " + content['action']
    try:
        signal_task.apply_async(args=[content['ticker'], content['interval'],
                                      content['action'], content['source']])
    except Exception as exc:
        print(exc)
        telegram_bot_task.apply_async(
            args=["🔴 EXCEPTION",
                  "GET /signal endpoint | failed starting signal_task"])
        telegram_bot_task.apply_async(args=["🔴 EXCEPTION", str(exc)])
        return str(exc)
    return 'Received Signal!'


@core.route('/restricted', methods=['GET'])
@require_appkey
def restricted():
    return 'Congratulations! Your core-app restricted route is running via your API key!'
