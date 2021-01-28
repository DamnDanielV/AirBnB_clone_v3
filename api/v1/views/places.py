#!/usr/bin/python3
""" CRUD for places"""
from flask import Flask, jsonify, abort, make_response, request
import json

from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_post_place(city_id):
    """ list places and creates a new one """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == "POST":
        place_json = request.get_json(silent=True)

        if place_json is None:
            return jsonify({"error": "Not a JSON"}), 400

        if "user_id" not in request.json:
            return jsonify({"error": "Missing user_id"}), 400

        if "name" not in request.json:
            return jsonify({"error": "Missing name"}), 400

        if not storage.get(User, place_json["user_id"]):
            abort(404)

        place_json["city_id"] = city_id
        n_place = Place(**place_json)
        storage.new(n_place)
        storage.save()
        storage.close()
        return jsonify(n_place.to_dict()), 201

    l_places = [place.to_dict() for place in city.places]
    return jsonify(l_places)


@app_views.route("/places/<place_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def gdp_place(place_id):
    """ CRUD places detal"""
    place = storage.get(Place, place_id)
    keys = ["id",
            "user_id",
            "city_id",
            "created_at",
            "updated_at"]
    if not place:
        abort(404)

    if request.method == "PUT":
        place_json = request.get_json(silent=True)

        if place_json is None:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in place_json.items():
            if key not in keys:
                setattr(place, key, value)

        storage.new(place)
        storage.save()
        storage.close()

    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        storage.close()
        return jsonify({})

    return jsonify(place.to_dict())
