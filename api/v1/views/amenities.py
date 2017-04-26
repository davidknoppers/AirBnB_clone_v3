#!/usr/bin/python3
"""
This module creates new view for Amenity objects that handles all default
RestFul API actions, get, post, put and delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


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
def get_an_amenity(amenity_id):
    """ Retrieves a Amenity object, based on id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_json())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a Amenity """
    content = request.get_json()
    if content is None:
        return "Not a JSON", 400
    if "name" not in content:
        return "Missing name", 400
    new_amenity = Amenity(name=content.get('name'))
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    content = request.get_json()
    if content is None:
        return "Not a JSON", 400
    amenity.name = content.get('name', amenity.name)
    amenity.save()
    return jsonify(amenity.to_json())
