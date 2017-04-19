#!/usr/bin/python3
"""
This module creates a new view for State objects that handles all default
RestFul API actions, get, post, put, delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/api/v1/states', methods=['GET'])
def get_state():
    """ Retrieves the list of all State objects """
    all_states = storage.all("State")
    states = []
    for key, value in all_states.items():
        states.append(value.to_json())
    return jsonify(states)

@app_views.route('/api/v1/states/<int:state_id>', methods=['GET'])
def get_a_state(state_id):
    """ Retrieves a State object based on given id """
    try:
        states = storage.all("State")
        for state in states:
            if state[0].get('id') == state_id:
                return jsonify(state.to_json()), 201
    except:
        abort(404)

@app_views.route('/api/v1/states/<int:state_id>', methods=['DELETE'])
def del_state(state_id):
    """ Deletes a State object """
    try:
        states = storage.all("State")
        for state in states:
            if state[0].get('id') == state_id:
                storage.delete(state)
                return jsonify({}), 201
    except:
        abort(404)

@app_views.route('/api/v1/states', methods=['POST'])
def create_state():
    """ Creates a State """
    if not request.get_json():
        return "Not a JSON", 404
    if not 'name' in request.get_json():
        return "Missing name", 404
    state = State(request.get_json())
    state.save()
    return jsonify({'state': state}), 201

@app_views.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State objec """
    if not request.get_json():
        return "Not a JSON", 404
    try:
        states = storage.all("State")
        for state in states:
            if state[0].get('id') == state_id:
                key_values = request.get_json()
                for k, value in key_values.items():
                    if k != "id" or k != "created_at" or k != "updated_at":
                        state[0][k] = value
                return jsonify({'state': state}), 201
    except:
        abort(404)
