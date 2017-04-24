#!/usr/bin/python3
from api.v1.views import app_views, Place, PlaceAmenity, storage
from flask import abort, jsonify, make_response, request
from os import getenv

"""
Interacts with Place and Amenity depending on the storage type
DBStorage: list, create and delete PlaceAmenity objects
FileStorage: list, add and remove Amenity IDs in
the list of amenities of a Place object
"""
storage_type = os.getenv("HBNB_TYPE_STORAGE", "fs")
if storage_type == "db":
    from models import PlaceAmenity

@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_all_amenities(place_id):
    """
    Gets all available amenities if place works properly
    """
    amenities = []
    if storage_type == "db":
        place = storage.get("Place", place_id)
        amenities = storage.all("Amenity")
        if place and amenities:
            try:
                for amenity in amenities.values():
                    print(amenity.place_amenities)
                return jsonify(amenities)
            except:
                abort(404)
    else:
        place = storage.get("Place", place_id)
        if place:
            amenity_ids = place.amenities
            try:
                for _id in amenity_ids:
                    new_am = storage.get("Amenity", _id).to_json()
                    amenities.append(new_am)
                return jsonify(amenities)
            except:
                abort(404)

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """
    deletes an amenity, in theory
    """
    place = storage.get("Place", place_id)
    if not place:
        print("place not found when trying to delete amenity")
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        return jsonify({}), 200

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity.place_id == place_id:
        return jsonify(amenity.to_json()), 200
    try:
        setattr(amenity, "place_id", place_id)
        return jsonify(amenity.to_json()), 201
    except:
        print("linking place to amenity failed")
        abort(404)
