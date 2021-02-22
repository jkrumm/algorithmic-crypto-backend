import json
from flask import Blueprint, current_app, render_template, session
from werkzeug.local import LocalProxy

from app.utils import requires_auth
from authentication import require_appkey
from app.public.forms import ExchangeConnection

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


@public.route('/setup')
@requires_auth
def setup():
    form = ExchangeConnection()
    return render_template('setup.html',
                           form=form,
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@public.route('/test', methods=['GET'])
def test():
    return 'Congratulations! Your core-app test route is running!'


@public.route('/restricted', methods=['GET'])
@require_appkey
def restricted():
    return 'Congratulations! Your public-app restricted route is running via your API key!'
