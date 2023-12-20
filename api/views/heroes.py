from flask import Blueprint

heroes = Blueprint("heroes", __name__, url_prefix="/api/v1/heroes")

@heroes.route("/register", methods=['POST'])
def register():
    return "Hero created"

@heroes.route("/me", methods=['GET'])
def me():
    return {"user": "me"}