#!/usr/bin/python3
""" CRUD for user """
from flask import Flask, request, jsonify, abort

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_post_user():
    """ list a user and creates a new one"""
    if request.method == "POST":
        user_json = request.get_json(silent=True)
        if not user_json:
            return jsonify({"error": "Not a JSON"}), 400

        if "password" not in user_json:
            return jsonify({"error": "Missing password"}), 400

        if "email" not in user_json:
            return jsonify({"error": "Missing email"}), 400

        new_user = User(**user_json)
        storage.new(new_user)
        storage.save()
        storage.close()
        return jsonify(new_user.to_dict()), 201
    users = storage.all(User)
    l_user = [user.to_dict() for user in users.values()]
    return jsonify(l_user)


@app_views.route("/users/<user_id>",
                 methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def gpd_user(user_id):
    """ CRUD user id """
    user = storage.get(User, user_id)
    keys = ["id", "updated_at", "created_at"]
    if not user:
        abort(404)

    if request.method == "PUT":
        user_json = request.get_json(silent=True)
        if user_json is None:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in user_json.items():
            if key not in keys:
                setattr(user, key, value)
        user.save()

    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        storage.close()
        return jsonify({})

    return jsonify(user.to_dict())
