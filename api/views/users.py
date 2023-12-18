from flask import Blueprint

users = Blueprint("users", __name__, url_prefix="/api/v1/users")

@users.route("/register", methods=['POST'])
def register():
    return "User created"

@users.route("/me", methods=['GET'])
def me():
    return {"user": "me"}