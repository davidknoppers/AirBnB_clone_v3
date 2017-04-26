#!/usr/bin/python3
"""
This module creates a new view for City objects that handles all default
RestFul API actions, get, post, put, delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state:
        all_cities = []
        cities = storage.all("City")
        for v in cities.values():
            if v.state_id == state_id:
                new_city = v.to_json()
                all_cities.append(new_city)
        return jsonify(all_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City """
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    elif r.get("name") is None:
        abort(400, "Missing name")
    state = storage.get("State", state_id)
    if state:
        r["state_id"] = state_id
        new_city = City(r)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_json()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    r = request.get_json()
    if r is None:
        abort(400, "Not a JSON")
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.name = r.get('name', city.name)
    city.save()
    return jsonify(city.to_json())
