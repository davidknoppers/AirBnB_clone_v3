#!/usr/bin/python3
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

"""
API functionality for Reviews. We can:
Retrieve all Review objects for a given Place
Retrieve/delete/create/update a single Review object

"""
storage_type = os.getenv("HBNB_TYPE_STORAGE", "fs")
if storage_type == "db":
    from models import PlaceAmenity

@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """
    Gets all available reviews if place works properly
    """
    review_output = []
    all_reviews = storage.all("Review")
@app_views.route("/reviews/<review_id>", methods=['GET'],
                  strict_slashes=False)
def return_review(review_id):
    """
    Attempts to retrieve and return
    a single review
    """
    review = storage.get("Review", review_id).to_json()
    if not review:
        print("retrieval of review failed")
        abort(404)
    return jsonify(review)

@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                  strict_slashes=False)
def del_review(review_id):
    try:
        review = storage.get("Review", review_id)
        storage.delete(review)
        storage.save()
        return jsonify({})
    except:
        abort(404)

@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                  strict_slashes=False)
def create_review():
    review_dict = request.get_json()
    if place_id not in review_dict:
        abort(404)
    try:
        place = storage.get("Place", place_id)
    except:
        abort(404)
    if user_id not in review_dict:
        return "Missing user_id", 400
    try:
        user = storage.get("User", user_id)
    except:
        abort(404)
    if "text" not in review_data:
        return "Missing text", 400
    new_review = Review(review_data)
    return jsonify(new_review.to_json())

@app_views.route("/reviews/<review_id>", methods=['PUT'],
                  strict_slashes=False)
def update_review():
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    try:
        review_data = request.get_json()
    except:
        abort(404)
    try:
        review = storage.get("Review", review_id)
    except:
        abort(404)
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
        storage.save()
    return jsonify(review.to_json())
