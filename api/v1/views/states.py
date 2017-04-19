#!/usr/bin/python3
"""
This module creates a new view for State objects that handles all default
RestFul API actions, get, post, put, delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    """ Retrieves the list of all State objects """
    all_states = storage.all("State")
    states = []
    for key, value in all_states.items():
        states.append(value.to_json())
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    """ Retrieves a State object based on given id """
    try:
        states = storage.all("State")
        for key, value in states.items():
            if value.to_json().get('id') == state_id:
                return jsonify(value.to_json())
    except:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """ Deletes a State object """
    try:
        states = storage.all("State")
        for key, value in states.items():
            if value.to_json().get('id') == state_id:
                storage.delete(state)
                return jsonify({}), 200
    except:
        abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    if not request.get_json():
        return "Not a JSON", 400
    if not 'name' in request.get_json():
        return "Missing name", 400
    state = State(request.get_json())
    state.save()
    return jsonify({'state': state}), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State objec """
    if not request.get_json():
        return "Not a JSON", 400
    try:
        states = storage.all("State")
        for key, value in states.items():
            if value.to_json().get('id') == state_id:
                key_values = request.get_json()
                for k, value in key_values.items():
                    if k != "id" or k != "created_at" or k != "updated_at":
                        value.to_json().get(k) = value
                return jsonify({'state': state}), 200
    except:
        abort(404)
