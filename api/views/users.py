from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from api.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from api.models.users import User
from api.database import db


users = Blueprint("users", __name__, url_prefix="/api/v1/users")

"""
    This is the registration endpoint.
    Users submit their details via this route.
"""

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

"""
    This is the login endpoint.
"""
@users.route('/login', methods=['POST'])
def login():
    email=request.json.get('email', ' ')
    password=request.json.get('password', ' ')

    user=User.query.filter_by(email=email).first()
    if user:
        is_password_correct=check_password_hash(user.password, password)
        if is_password_correct:
            refresh=create_refresh_token(identity=user.id)
            access=create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.userName,
                    'email': user.email
                }
            }), HTTP_200_OK
    return jsonify({
        'error': "Invalid credentials provided"
    }), HTTP_401_UNAUTHORIZED

@users.route("/me", methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()
    return jsonify({
        'username':user.userName,
        'email':user.email
    }), HTTP_200_OK 
