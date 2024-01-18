from flask import Blueprint, request, jsonify
from api.models.heroes import Hero
from api.database import db
from api.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from api.models.heroes import Hero

heroes = Blueprint("heroes", __name__, url_prefix="/api/v1/heroes")

@heroes.route("/create_hero_profile", methods=['POST'])
def create_hero_profile():
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
              achievements=achievements)
    # Creating our hero into the database
    db.session.add(hero)
    # Committing/saving changes into the database
    db.session.commit()

    return jsonify({
        'message':"Hero created successfully",
        'First name':hero.firstName,
        'Last name':hero.lastName
    }), HTTP_201_CREATED

