#!/usr/bin/python3
""" CRUD for cities """
from flask import Flask, jsonify, abort, make_response, request
import json

from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_post_city(state_id):
    """list cities from a state and creates a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == "POST":
        city_json = request.get_json(silent=True)

        if city_json is None:
            return jsonify({"error": "Not a JSON"}), 400

        if "name" not in request.json:
                return jsonify({"error": "Missing name"}), 400
        city_json["state_id"] = state_id
        new_city = City(**city_json)
        storage.new(new_city)
        storage.save()
        storage.close()
        return jsonify(new_city.to_dict()), 201

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def gdp_city(city_id):
    """GET DELETE PUT a city"""
    city = storage.get(City, city_id)
    keys = ["id", "state_id", "created_at", "updated_at"]
    if not city:
        abort(404)

    if request.method == "PUT":
        city_json = request.get_json(silent=True)

        if city_json is None:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in city_json.items():
            if key not in keys:
                setattr(city, key, value)
        storage.new(city)
        storage.save()
        storage.close()

    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        storage.close()
        return jsonify({})

    return jsonify(city.to_dict())
