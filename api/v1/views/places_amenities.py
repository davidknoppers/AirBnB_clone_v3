#!/usr/bin/python3
"""
Interacts with Place and Amenity depending on the storage type
DBStorage: list, create and delete PlaceAmenity objects
FileStorage: list, add and remove Amenity IDs in
the list of amenities of a Place object
"""


from api.v1.views import app_views, Place, storage
from flask import abort, jsonify, make_response, request
from os import getenv
from sqlalchemy import inspect


storage_type = getenv("HBNB_TYPE_STORAGE", "fs")
if storage_type == "db":
    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def get_all_amenities_db(place_id):
        """gets all amenities within a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenities = []
        for amenity in place.amenities:
            amenities.append(amenity.to_json())
        return jsonify(amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity_db(place_id=None, amenity_id=None):
        """deletes an amenity within a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        try:
            place.amenities.remove(amenity)
            place.save()
            return jsonify({}), 200
        except:
            abort(404)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity_db(place_id=None, amenity_id=None):
        """links an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_json()), 201

else:

    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def get_all_amenities_fs(place_id):
        """get all amenities within a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenities = []
        for amenity in place.amenities:
                amenities.append(amenity)
        return jsonify(amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity_fs(place_id=None, amenity_id=None):
        """delete an amenity within a place"""
        place_check = storage.get("Place", place_id)
        amenity_check = storage.get("Amenity", amenity_id)
        if place_check is None or amenity_check is None:
            abort(404)
        for amenity in place.amenities:
            if amenity == amenity_id:
                storage.delete(amenity_check)
                return jsonify({}), 200
        abort(404)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity_fs(place_id=None, amenity_id=None):
        """link an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        for amenities_id in place.amenities:
            """
            if item already exists, return it
            """
            if amenity_id == amenities_id:
                return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity_id)
        place.save()
        return jsonify(amenity.to_json()), 201
