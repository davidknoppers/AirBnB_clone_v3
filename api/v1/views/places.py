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
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    place = storage.all("Place")
    places = []
    for value in place.values():
        if value.city_id == city_id:
            places.append(value.to_json())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_place(place_id):
    """ Retrieves a Place object, based on id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    if not request.get_json():
        abort(400, "Not a JSON")
    if not 'user_id' in request.get_json():
        abort(400, "Missing user_id")
    if not 'name' in request.get_json():
        abort(400, "Missing name")
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    place = request.get_json()
    user = storage.get("User", place["user_id"])
    if not user:
        abort(404)
    place["city_id"] = city_id
    new_place = Place(place)
    new_place.save()
    created_place = storage.get("Place", new_place.id)
    return jsonify(created_place.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a Place """
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.name = r.get('name', place.name)
    place.description = r.get('description', place.description)
    place.number_rooms = r.get('number_rooms', place.number_rooms)
    place.number_bathrooms = r.get('number_bathrooms', place.number_bathrooms)
    place.max_guest = r.get('max_guest', place.max_guest)
    place.price_by_night = r.get('price_by_night', place.price_by_night)
    place.latitude = r.get('latitude', place.latitude)
    place.longitude = r.get('longitude', place.longitude)
    place.save()
    return jsonify(place.to_json()), 200
