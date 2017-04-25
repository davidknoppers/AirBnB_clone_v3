#!/usr/bin/python3
from api.v1.views import app_views, Place, PlaceAmenity, storage
from flask import abort, jsonify, make_response, request
from os import getenv
from sqlalchemy import inspect

"""
Interacts with Place and Amenity depending on the storage type
DBStorage: list, create and delete PlaceAmenity objects
FileStorage: list, add and remove Amenity IDs in
the list of amenities of a Place object
"""
storage_type = getenv("HBNB_TYPE_STORAGE", "fs")
if storage_type == "db":
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def get_all_amenities_db(place_id):
        """gets all amenities within a place"""
        place = storage.get("Place", place_id)
        if not place:
            abort(404)
        amenities = []
        for amenity in place.amenities:
            amenities.append(amenity.to_json())
        return jsonify(amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['DELETE'])
    def delete_placeamenity_db(place_id=None, amenity_id=None):
        """deletes an amenity within a place"""
        place = storage.get("Place", place_id)
        if not place:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity:
            place.amenities.remove(amenity)
            place.save()
            return jsonify(place.amenities), 200
        return jsonify({}), 200

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['POST'])
    def create_amenity_db(place_id=None, amenity_id=None):
        """links an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            return "Bad place", 404
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            return "Bad amenity", 404
        if amenity in place.amenities:
            return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity)
        place.save()
        storage.save()
        return jsonify(amenity.to_json()), 201

else:

    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def get_all_amenities_fs(place_id):
        """get all amenities within a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        result = [storage.get("Amenity", i) for i in place.amenities]
        return jsonify(result)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['DELETE'])
    def delete_placeamenity_fs(place_id=None, amenity_id=None):
        """delete an amenity within a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        if amenity_id is not None:
            for i in range(len(place.amenities)):
                if place.amenity[i] == amenity_id:
                    place.amenity.pop(i)
                    place.save()
        return jsonify({}), 200

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['POST'])
    def create_amenity_fs(place_id=None, amenity_id=None):
        """link an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            return "Bad amenity", 404
        for amenity in place.amenities:
            """
            if item already exists, return it
            """
            if amenity_id == amenity:
                return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity_id)
        place.save()
        return jsonify(amenity.to_json()), 201
