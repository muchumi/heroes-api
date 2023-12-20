from flask import Flask, jsonify
import os
from api.views.users import users
from api.views.heroes import heroes

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(users)
    app.register_blueprint(heroes)

    return app


