from flask import Flask, jsonify
from flask_cors import CORS
from logic.logic import db

app = Flask(__name__)
CORS(app)

db.init_app(app)


@app.route('/')
def main_route():
    print("received call")
    return 'response from root'


@app.errorhandler(400)
def page_not_found(e):
    print(dict(e))
    return jsonify(status="error", error_type="400"), 400


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return jsonify(status="error", error_type="404"), 404


@app.errorhandler(410)
def internal_error(e):
    print(e)
    return jsonify(status="error", error_type="410"), 410


@app.errorhandler(500)
def internal_error(e):
    print(e)
    return jsonify(status="error", error_type="500"), 500
