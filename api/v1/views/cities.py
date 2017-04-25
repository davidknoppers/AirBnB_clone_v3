#!/usr/bin/python3
"""
This module creates a new view for City objects that handles all default
RestFul API actions, get, post, put, delete.
"""
from api.v1.views import app_views
from api.v1.views import page_not_found
from flask import abort, jsonify, request
from models import *


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    try:
        state = storage.get("State", state_id)
        if state:
            all_cities = []
            cities = storage.all("City")
            for v in cities.values():
                if v.state_id == state_id:
                    new_city = v.to_json()
                    all_cities.append(new_city)
            return jsonify(all_cities)
    except:
        return(page_not_found(404))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object.
    """
    try:
        city = storage.get("City", city_id)
        return jsonify(city.to_json())
    except:
        return(page_not_found(404))


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    try:
        city = storage.get("City", city_id)
        storage.delete(city)
        return jsonify({}), 200
    except:
        return(page_not_found(404))


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City """
    if not request.get_json():
        return abort(400), "Not a JSON"
    if not 'name' in request.get_json():
        return abort(400), "Missing name"
    try:
        state = storage.get("State", state_id)
        if state:
            city = request.get_json()
            city["state_id"] = state_id
            new_city = City(city)
            new_city.save()
            created_city = storage.get("City", new_city.id)
            return jsonify(created_city.to_json()), 201
    except:
        return(page_not_found(404))


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    if not request.get_json():
        return abort(400), "Not a JSON"
    try:
        skip_list = ["id", "created_at", "updated_at", "state_id"]
        city = storage.get("City", city_id)
        city = city.to_json()
        key_values = request.get_json()
        for k, v in key_values.items():
            if k not in skip_list:
                city[k] = v
        return jsonify(city), 200
    except:
        return(page_not_found(404))
