#!/usr/bin/python3
"""
This module creates new view for User objects that handles all default
RestFul API actions, get, post, put and delete.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_user():
    """ Retrieves the list of all User objects """
    user = storage.all("User")
    users = []
    for value in user.values():
        users.append(value.to_json())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_user(user_id):
    """ Retrieves a User object, based on id """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    if not request.get_json():
        abort(400, "Not a JSON")
    if not 'email' in request.get_json():
        abort(400, "Missing email")
    if not 'password' in request.get_json():
        abort(400, "Missing password")
    user = User(request.get_json())
    user.save()
    new_user = storage.get("User", user.id)
    return jsonify(new_user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a User  """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    skip_list = ["id", "email", "created_at", "updated_at"]
    key_values = request.get_json()
    user = user.to_json()
    for k, v in key_values.items():
        if k not in skip_list:
            user[k] = v
    return jsonify(user)
