#!/usr/bin/python3
""" CRRUD review"""
import json
from flask import Flask, jsonify, abort, make_response, request

from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_post_review(place_id):
    """ list and creates a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == "POST":
        review_json = request.get_json(silent=True)
        if review_json is None:
            return jsonify({"error": "Not a JSON"}), 400

        if "text" not in request.json:
            return jsonify({"error": "Missing text"}), 400

        if "user_id" not in request.json:
            return jsonify({"error": "Missing user_id"}), 400

        if not storage.get(User, review_json["user_id"]):
            abort(404)

        review_json["place_id"] = place_id
        n_review = Review(**review_json)
        storage.new(n_review)
        storage.save()
        storage.close()
        return jsonify(n_review.to_dict()), 201

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def review_detail(review_id):
    """ CRUD review view """
    review = storage.get(Review, review_id)
    keys = ["id",
            "user_id",
            "place_id",
            "created_at",
            "updated_at"]
    if not review:
        abort(404)

    if request.method == "PUT":
        review_json = request.get_json(silent=True)

        if review_json is None:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in review_json.items():
            if key not in keys:
                setattr(review, key, value)

        storage.new(review)
        storage.save()
        storage.close()

    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        storage.close()
        return jsonify({}), 200

    return jsonify(review.to_dict())
