#!/usr/bin/python3
"""
This module creates new view for Place objects that handles all default
RestFul API actions, get, post, put and delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_place(city_id):
    """ Retrieves the list of all Place objects of a City """
    try:
        city = storage.get("City", city_id)
        if city:
            place = storage.all("Place")
            places = []
            for value in place.values():
                if value.city_id == city_id:
                    places.append(value.to_json())
            return jsonify(places)
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_place(place_id):
    """ Retrieves a Place object, based on id """
    try:
        place = storage.get("Place", place_id)
        return jsonify(place.to_json())
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    try:
        place = storage.get("Place", place_id)
        storage.delete(place)
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    if not request.get_json():
        return "Not a JSON", 400
    if not 'user_id' in request.get_json():
        return "Missing user_id", 400
    if not 'name' in request.get_json():
        return "Missing name", 400
    try:
        city = storage.get("City", city_id)
        if city:
            place = request.get_json()
            user = storage.get("User", place["user_id"])
            if not user:
                abort(404)
            place["city_id"] = city_id
            new_place = Place(place)
            new_place.save()
            created_place = storage.get("Place", new_place.id)
            return jsonify(created_place.to_json()), 201
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a Place """
    if not request.get_json():
        return "Not a JSON", 400
    try:
        place = storage.get("Place", place_id).to_json()
        skip_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
        key_values = request.get_json()
        for k, v in key_values.items():
            if k not in skip_list:
                place[k] = v
        return jsonify(place), 200
    except:
        abort(404)
