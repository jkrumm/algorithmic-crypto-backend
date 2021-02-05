from app.auth.views import auth


def register_route_blueprint(app):
    app.register_blueprint(auth, url_prefix="/auth")
