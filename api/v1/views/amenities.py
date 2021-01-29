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
                 methods=["GET"],
                 strict_slashes=False)
def get_amenity():
    """get an amenity"""
    amenities = storage.all(Amenity)
    l_amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(l_amenities)


@app_views.route("/amenities",
                 methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """POST method"""
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, "Not a JSON")

    if "name" not in request.json:
        abort(400, "Missing name")

    n_amenity = Amenity(**amenity_json)
    n_amenity.save()
    return jsonify(n_amenity.to_dict()), 201


# @app_views.route("/amenities",
#                  methods=["GET", "POST"],
#                  strict_slashes=False)
# def get_post_amenity():
#     """list amenities from a state and creates a new city"""
#     if request.method == "POST":
#         amenity_json = request.get_json(silent=True)
#         if amenity_json is None:
#             abort(400, "Not a JSON")

#         if "name" not in request.json:
#             abort(400, "Missing name")

#         n_amenity = Amenity(**amenity_json)
#         storage.new(n_amenity)
#         storage.save()
#         storage.close()
#         return jsonify(n_amenity.to_dict()), 201

#     elif request.method == "GET":

#         amenities = storage.all(Amenity)
#         l_amenities = [amenity.to_dict() for amenity in amenities.values()]
#         return jsonify(l_amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_ame_id(amenity_id):
    """get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return (jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_ame_id(amenity_id):
    """put method"""
    amenity = storage.get(Amenity, amenity_id)

    amenity_json = request.get_json(silent=True)
    keys = ["id", "created_at", "updated_at"]

    if amenity_json is None:
        abort(400, "Not a JSON")

        for key, value in amenity_json.items():
            if key not in keys:
                setattr(amenity, key, value)
        amenity.save()
    return (jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def del_ame_id(amenity_id):
    """delete an amaenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity_json is None:
        abort(400, "Not a JSON")

    storage.delete(amenity)
    storage.save()
    storage.close()
    return (jsonify(amenity.to_dict()), 200)


# @app_views.route("/amenities/<amenity_id>",
#                  methods=["GET", "PUT", "DELETE"],
#                  strict_slashes=False)
# def gdp_amenity(amenity_id):
#     """GET DELETE PUT for amenity"""
#     amenity = storage.get(Amenity, amenity_id)
#     keys = ["id", "created_at", "updated_at"]
#     if not amenity:
#         abort(404)

#     if request.method == "PUT":
#         amenity_json = request.get_json(silent=True)

#         if amenity_json is None:
#             abort(400, "Not a JSON")

#         for key, value in amenity_json.items():
#             if key not in keys:
#                 setattr(amenity, key, value)
#         amenity.save()

#     elif request.method == "DELETE":
#         storage.delete(amenity)
#         storage.save()
#         storage.close()
#         return make_response(jsonify({}), 200)

#     return make_response(jsonify(amenity.to_dict()), 200)
