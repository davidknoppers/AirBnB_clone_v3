#!/usr/bin/python3
"""
Basic setup to return count of each class in db
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({'status': "Ok"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    from models import storage
    obj_counts = {}
    classes = self.__models_available.keys()
    for cls in classes:
        obj_counts[cls] = self.count(cls)
    return obj_counts
    """
    from models import storage
    models_available = ["User", "Amenity", "City", "Place", "Review", "State"]
    formats = {"User": "users", "Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews", "State": "states"}
    output = {}
    for model in models_available:
        output[formats[model]] = storage.count(model)
    return jsonify(output)
