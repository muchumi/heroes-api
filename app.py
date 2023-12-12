from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return "Hello world"

@app.route("/home", methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Home Page"
    })