#!/usr/bin/python3
"""
This module creates a new view for City objects that handles all default
RestFul API actions, get, post, put, delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    try:
        state = storage.get("State", state_id)
    except:
        abort(404)
    all_cities = []
    cities = storage.all("City")
    for k, v in cities.items():
        if v.state_id == state_id:
            all_cities.append(v.to_json())
    return jsonify(all_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object.
    """
    try:
        city = storage.get("City", city_id)
        return jsonify(city.to_json())
    except:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    try:
        city = storage.get("City", city_id)
        storage.delete(city)
        return jsonify({}), 200
    except:
        abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a State """
    if not request.get_json():
        return "Not a JSON", 400
    if not 'name' in request.get_json():
        return "Missing name", 400
    try:
        state = storage.get("State", state_id)
    except:
        abort(404)
    city = request.get_json()
    city["state_id"] = state_id
    city = City(city)
    city.save()
    created_city = storage.get("City", city.id).to_json()
    return jsonify(created_city), 201

@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    if not request.get_json():
        return "Not a JSON", 400
    try:
        city = storage.get("City", city_id).to_json()
        key_values = request.get_json()
        for k, v in key_values.items():
            if k != "id" or k != "created_at" or k != "updated_at" or k != "state_id":
                city[k] = v
        return jsonify(city), 200
    except:
        abort(404)
