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
    for value in all_states.values():
        states.append(value.to_json())
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    """ Retrieves a State object based on given id """
    try:
        state = storage.get("State", state_id)
        return jsonify(state.to_json())
    except:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """ Deletes a State object """
    try:
        state = storage.get("State", state_id)
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
    new_state = storage.get("State", state.id)
    return jsonify(new_state.to_json()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State objec """
    if not request.get_json():
        return "Not a JSON", 400
    try:
        state = storage.get("State", state_id).to_json()
        skip_list = ["id", "created_at", "updated_at"]
        key_values = request.get_json()
        for k, v in key_values.items():
            if k not in skip_list:
                state[k] = v
        return jsonify(state), 200
    except:
        abort(404)
