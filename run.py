from werkzeug.exceptions import HTTPException
from flask import jsonify, redirect, session, url_for
from app import create_app
from app.config import BaseConfig

from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

app = create_app()


# @app.errorhandler(Exception)
# def handle_auth_error(ex):
#     response = jsonify(message=str(ex))
#     response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
#     return response


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=BaseConfig.AUTH0_CLIENT_ID,
    client_secret=BaseConfig.AUTH0_CLIENT_SECRET,
    api_base_url='https://' + BaseConfig.AUTH0_DOMAIN,
    access_token_url='https://' + BaseConfig.AUTH0_DOMAIN + '/oauth/token',
    authorize_url='https://' + BaseConfig.AUTH0_DOMAIN + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=BaseConfig.AUTH0_CALLBACK_URL)


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('public.home', _external=True),
              'client_id': BaseConfig.AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/status', methods=['GET'])
def status():
    return 'Running!'


if __name__ == '__main__':
    app.run()
