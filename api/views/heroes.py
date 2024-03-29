from flask import Blueprint, request, jsonify
from api.models.heroes import Hero, hero_schema, heroes_schema
from api.database import db
from api.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from flask_jwt_extended import get_jwt_identity, jwt_required

heroes = Blueprint("heroes", __name__, url_prefix="/api/v1/heroes")

"""
    This is the create hero profile endpoint.
    Users are able to create profiles of their heroes.
"""

@heroes.route("/create_hero_profile", methods=['POST'])
@jwt_required()
def create_hero_profile():
    current_user=get_jwt_identity()

    firstName=request.json["firstName"]
    lastName=request.json["lastName"]
    service_number=request.json["service_number"]
    year_of_birth=request.json["year_of_birth"]
    education=request.json["education"]
    achievements=request.json["achievements"]

    if Hero.query.filter_by(service_number=service_number).first():
        return jsonify({
            'error': "Service number {service_number} is already taken"
        }), HTTP_409_CONFLICT

    hero=Hero(firstName=firstName, lastName=lastName, year_of_birth=year_of_birth, education=education,
              achievements=achievements, user_id=current_user)
    # Creating our hero into the database
    db.session.add(hero)
    # Committing/saving changes into the database
    db.session.commit()

    return jsonify({
        'message':"Hero created successfully",
        'id':hero.id,
        'First name':hero.firstName,
        'Last name':hero.lastName,
        'Service number':hero.service_number
    }), HTTP_201_CREATED

"""
    This is the get all heroes route.
    This endpoint allows users retrieve a list of all heroes saved in the database.
"""
@heroes.route("/", methods=['GET'])
@jwt_required()
def get_all_heroes():
    current_user=get_jwt_identity()
    all_heroes=Hero.query.filter_by(user_id=current_user)
    return heroes_schema.dump(all_heroes), HTTP_200_OK

"""
    This endpoint retrieves a single hero.
    It retrieves a single hero by his id.
"""
@heroes.route("/<int:id>", methods=['GET'])
@jwt_required()
def get_a_hero(id):
    current_user=get_jwt_identity()
    hero=Hero.query.filter_by(user_id=current_user, id=id).first()

    if not hero:
        return jsonify({
            'error':"Hero not found"
        }), HTTP_404_NOT_FOUND
    return hero_schema.dump(hero), HTTP_200_OK

"""
    This is the edit hero endpoint.
    It allows user to modify hero details in the database.
"""
@heroes.route("/edit_hero/<int:id>", methods=['PUT'])
@jwt_required()
def edit_hero(id):
    current_user=get_jwt_identity()
    hero=Hero.query.filter_by(user_id=current_user, id=id).first()

    if not hero:
        return jsonify({
            'error':"Hero not found"
        }), HTTP_404_NOT_FOUND
    
    firstName=request.json['firstName']
    lastName=request.json['lastName']
    service_number=request.json['service_number']
    year_of_birth=request.json['year_of_birth']
    education=request.json['education']
    achievements=request.json['achievements']

    hero.firstName=firstName
    hero.lastName=lastName
    hero.service_number=service_number
    hero.year_of_birth=year_of_birth
    hero.education=education
    hero.achievements=achievements

    db.session.commit()

    return hero_schema.dump(hero), HTTP_200_OK

"""
    This is the delete a hero endpoint.
    It allows users to delete records of heroes by id.
"""  
@heroes.route("/delete_hero/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_hero(id):
    current_user=get_jwt_identity()
    hero=Hero.query.filter_by(user_id=current_user, id=id).first()

    if not hero:
        return jsonify({
            'error': "Hero not found"
        }), HTTP_404_NOT_FOUND
    else:
        db.session.delete(hero)
        db.session.commit()
        return jsonify({
            'message': "Hero record has been deleted successfully."
        }), HTTP_200_OK
    