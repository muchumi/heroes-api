from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from api.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED
import validators
from api.models.users import User
from api.database import db


users = Blueprint("users", __name__, url_prefix="/api/v1/users")

@users.route("/register", methods=['POST'])
def register():
    firstName=request.json["firstName"]
    lastName=request.json["lastName"]
    userName=request.json["userName"]
    email=request.json["email"]
    password=request.json["password"]

    if len(password)<8:
        return jsonify({
            'error': "Password is too short"
        }), HTTP_400_BAD_REQUEST
    
    if len(userName)<5:
        return jsonify({
            'error': "Username is too short"
        }), HTTP_400_BAD_REQUEST
    
    if not userName.isalnum() or " " in userName:
        return jsonify({
            'error': "Username should be alphanumeric and no spaces"
        }), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({
            'error': "Email is not valid"
        }), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error': "Email is taken"
        }), HTTP_409_CONFLICT
    
    if User.query.filter_by(userName=userName).first() is not None:
        return jsonify({
            'error': "Username is taken"
        }), HTTP_409_CONFLICT
    
    password_hash=generate_password_hash(password)

    user=User(firstName=firstName, lastName=lastName, userName=userName, email=email, password=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'message': "User created successfully",
        'user': {
            'username': userName,
            'email': email
        }
    }), HTTP_201_CREATED

@users.route("/me", methods=['GET'])
def me():
    return {"user": "me"}