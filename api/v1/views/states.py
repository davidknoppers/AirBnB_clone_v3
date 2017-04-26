#!/usr/bin/python3
"""
This module creates a new view for State objects that handles all default
RestFul API actions, get, post, put, delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves the list of all State objects """
    all_states = storage.all("State")
    states = []
    for value in all_states.values():
        states.append(value.to_json())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id=None):
    """ Retrieves a State object based on given id """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id=None):
    """ Deletes a State object """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    content = request.get_json()
    if content is None:
        return "Not a JSON", 400
    elif content.get("name") is None:
        return "Not a JSON", 400
    new_state = State(name=content['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """updates a state object"""
    if state_id is None:
        abort(404)
    r = request.get_json()
    if r is None:
        return "Not a JSON", 400
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.name = r.get('name', state.name)
    state.save()
    return jsonify(state.to_json())
