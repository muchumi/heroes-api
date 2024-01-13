from flask import Blueprint, request, jsonify
from api.models.heroes import Hero
from api.database import db
from api.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED

heroes = Blueprint("heroes", __name__, url_prefix="/api/v1/heroes")

@heroes.route("/create_hero_profile", methods=['POST'])
def create_hero_profile():
    firstName=request.json["firstName"]
    lastName=request.json["lastName"]
    year_of_birth=request.json["year_of_birth"]
    education=request.json["education"]
    achievements=request.json["achievements"]

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

