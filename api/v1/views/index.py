#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({'status': "Ok"})


@app_views.route('/api/v1/stats')
def stats():
    return "storage.get"
