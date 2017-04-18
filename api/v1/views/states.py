#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import *


@app_views.route('/api/v1/states', methods=['GET'])
def get_state():
    """ Retrieves the list of all State objects """
    return storage.all("State").to_json()

@app_views.route('/api/v1/states/<int:state_id>', methods=['GET'])
def get_a_state():
    """ Retrieves a State object based on given id """
    try:
        states = storage.all("State").values
        return 
    except:
        abort(404)

@app_views.route('/api/v1/states/<int:state_id>', methods=['DELETE'])
def del_state():
    """ Deletes a State object """
    try:
        states = storage.all("State").values
        return {}
    except:
        abort(404)

@app_views.route('/api/v1/states', methods=['POST'])
def create_state():
    """ Creates a State """
    if not request.get_json:
        abort("Not a JSON", 404)
    state = {
    }
    states.append(state)
    return jsonify({}), 201
