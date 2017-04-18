#!/usr/bin/python3
"""
This module starts a rest api.
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def store_close(exception=None):
    """  """
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': "Not found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
