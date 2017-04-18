#!/usr/bin/python3
"""
Basic setup to return count of each class in db
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({'status': "Ok"})


@app_views.route('/api/v1/stats')
def stats():
    from models import storage
    obj_counts = {}
    classes = self.__models_available.keys()
    for cls in classes:
        obj_counts[cls] = self.count(cls)
    return obj_counts
