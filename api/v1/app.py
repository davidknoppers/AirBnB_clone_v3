#!/usr/bin/python3
"""
This module starts a rest api.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def store_close(exception=None):
    """ closes the storage on exit """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Custom 404 handler in Json"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.environ.get('HBNB_API_HOST'),
            port=os.environ.get('HBNB_API_PORT'))
