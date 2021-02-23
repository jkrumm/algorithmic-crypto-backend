import json
import ccxt
from flask import Blueprint, current_app, render_template, session, request, \
    redirect, url_for
from werkzeug.local import LocalProxy

from app.utils import requires_auth, encrypt, change_user_app_metadata
from authentication import require_appkey
from app.public.forms import ExchangeConnection
from app.config import BaseConfig

public = Blueprint('public', __name__, template_folder='templates')
logger = LocalProxy(lambda: current_app.logger)


@public.before_request
def before_request_func():
    current_app.logger.name = 'public'


@public.route('/')
def home():
    return render_template('home.html')


@public.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@public.route('/setup', methods=['GET', 'POST'])
@requires_auth
def setup():
    form = ExchangeConnection(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        exchange_connection = {
            "exchange": form.exchange.data,
            "bot": form.bot.data,
            "api_key": form.api_key.data,
            "api_secret": encrypt(form.api_secret.data)
        }
        try:
            kraken = ccxt.kraken({
                'apiKey': form.api_key.data,
                'secret': form.api_secret.data,
                'enableRateLimit': True,
                "timeout": 100000,
                'options': {
                    'fetchMinOrderAmounts': False
                }
            })
            kraken.fetch_balance()
            logger.info(str(exchange_connection))
            logger.info(session['profile']['user_id'])
            change_user_app_metadata(session['profile']['user_id'], exchange_connection)
            return redirect(url_for('public.dashboard'))
        except:
            return render_template(
                'setup.html', form=form,
                error="Invalid " + form.exchange.data + " api credentials.",
                userinfo=session['profile'],
                userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
    else:
        return render_template(
            'setup.html', form=form, error=None, userinfo=session['profile'],
            userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


@public.route('/test', methods=['GET'])
def test():
    return 'Congratulations! Your core-app test route is running!'


@public.route('/restricted', methods=['GET'])
@require_appkey
def restricted():
    return 'Congratulations! Your public-app restricted route is running via your API key!'
