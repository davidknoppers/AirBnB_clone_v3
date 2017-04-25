#!/usr/bin/python3
"""
This module creates new view for Amenity objects that handles all default
RestFul API actions, get, post, put and delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenity():
    """ Retrieves the list of all Amenity objects """
    amenity = storage.all("Amenity")
    amenities = []
    for value in amenity.values():
        amenities.append(value.to_json())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_amenity(amenity_id):
    """ Retrieves a Amenity object, based on id """
    try:
        amenity = storage.get("Amenity", amenity_id)
        return jsonify(amenity.to_json())
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    try:
        amenity = storage.get("Amenity", amenity_id)
        storage.delete(amenity)
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a Amenity """
    if not request.get_json():
        return "Not a JSON", 400
    if not 'name' in request.get_json():
        return "Missing name", 400
    amenity = Amenity(request.get_json())
    amenity.save()
    new_amenity = storage.get("Amenity", amenity.id)
    return jsonify(new_amenity.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity """
    if not request.get_json():
        return "Not a JSON", 400
    try:
        amenity = storage.get("Amenity", amenity_id).to_json()
        skip_list = ["id", "created_at", "updated_at"]
        key_values = request.get_json()
        for k, v in key_values.items():
            if k not in skip_list:
                amenity[k] = v
        return jsonify(amenity), 200
    except:
        abort(404)
