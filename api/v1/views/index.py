#!/usr/bin/python3
"""index page JSON"""

from flask import jsonify

from api.v1.views import app_views
from models import storage


# create a route /status on the object app_views
# that returns a JSON: "status": "OK"
@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


# Create an endpoint that retrieves the number of each objects by type
@app_views.route("/stats", strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    c = {}
    mod = {
            "amenities": "Amenity", "cities": "City",
            "places": "Place", "reviews": "Review",
            "states": "State", "users": "User"
            }

    for key, value in mod.items():
        c[key] = storage.count(value)
    return jsonify(c)
