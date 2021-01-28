#!/usr/bin/python3
""" CRUD for cities """
from flask import Flask, jsonify, abort, make_response, request
import json

from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_post_amenity():
    """list cities from a state and creates a new city"""
    if request.method == "POST":
        amenity_json = request.get_json(silent=True)
        if amenity_json is None:
            abort(400, "Not a JSON")

        if "name" not in request.json:
            abort(400, "Missing name")

        n_amenity = Amenity(**amenity_json)
        storage.new(n_amenity)
        storage.save()
        storage.close()
        return jsonify(n_amenity.to_dict()), 201

    amenities = storage.all(Amenity)
    l_amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(l_amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def gdp_amenity(amenity_id):
    """GET DELETE PUT for amenity"""
    amenity = storage.get(Amenity, amenity_id)
    keys = ["id", "state_id", "created_at", "updated_at"]
    if not amenity:
        abort(404)

    if request.method == "PUT":
        amenity_json = request.get_json(silent=True)

        if amenity_json is None:
            abort(400, "Not a JSON")

        for key, value in amenity_json.items():
            if key not in keys:
                setattr(amenity, key, value)
        amenity.save()

    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        storage.close()
        return make_response(jsonify({}), 200)

    return jsonify(amenity.to_dict())
