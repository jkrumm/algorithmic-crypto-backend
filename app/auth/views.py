from flask import Blueprint


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET"])
def login():
    return "true un auth"
