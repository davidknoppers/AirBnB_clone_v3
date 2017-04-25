#!/usr/bin/python3
"""
API functionality for Reviews. We can:
Retrieve all Review objects for a given Place
Retrieve/delete/create/update a single Review object
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, Review


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """
    Gets all available reviews if place exists
    and has reviews
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for r in place.reviews:
        reviews.append(r.to_json())
    return(jsonify(reviews))


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def single_review(review_id):
    """
    Attempts to retrieve and return
    a single review
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    deletes a review from a place
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a user review for a valid place
    Requires a valid place_id and user_id
    """
    try:
        review_dict = request.get_json()
    except:
        return "Not a JSON", 400
    if not review_dict:
        abort(404)
    if place_id not in review_dict:
        abort(404)
    if "user_id" not in review_dict.keys():
        return "Missing user_id", 400
    if "text" not in review_dict.keys():
        return "Missing text", 400
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    user = storage.get("User", review_dict["user_id"])
    if not user:
        abort(404)
    review = Review(**review_dict)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_json()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    updates a review if place and attributes are valid
    """
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    try:
        review_dict = request.get_json()
    except:
        return "Not a JSON", 400
    for key, value in review_dict.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_json()), 200
