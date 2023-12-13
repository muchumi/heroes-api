from flask import Flask, jsonify

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY="dev",
        )
    else:
        app.config.from_mapping(test_config)

    @app.route("/", methods=['GET'])
    def index():
        return "Hello world"

    @app.route("/home", methods=['GET'])
    def home():
        return jsonify({
            "message": "Welcome to the Home Page"
        })

    return app


