#!/usr/bin/python3
"""handles CRUD to State"""

from flask import abort, jsonify, make_response, request

from models import storage
from models.state import State
from api.v1.views import app_views


# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route("/states",
                 methods=["GET"],
                 strict_slashes=False)
def get_st():
    return jsonify([value.to_dict() for key, value in storage.all("State")
                    .items()])


# Retrieves a State object: GET /api/v1/states/<state_id>
@app_views.route("/states/<state_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_id_st(state_id):
    state = [value.to_dict() for key, value in storage.all("State")
             .items() if key == 'State.' + state_id]

    if state[0] is None:
        abort(404)
    return jsonify(state[0])


# Deletes a State object:: DELETE /api/v1/states/<state_id>
@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def del_st(state_id):
    state = storage.get(state_id)   # line 72 file_storage
    if not state:
        abort(404)

    storage.delete(state)   # line 61 file_storage
    storage.save()  # line 43 file_storage
    return make_response(jsonify({}), 200)


# Creates a State: POST /api/v1/states
@app_views.route("/states/",
                 methods=["POST"],
                 strict_slashes=False)
def post_st():
    dic_n = request.get_json(silent=True)   # https://tedboy.github.io/flask/
    # generated/generated/flask.Request.get_json.html
    if dic_n is None:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400

    state = State(**dic_n)
    storage.new(state)  # line 37 file_storage
    storage.save()
    return jsonify(state.to_dict()), 201


# Updates a State object: PUT /api/v1/states/<state_id>
@app_views.route("/states/<state_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_st(state_id):
    dict_st = request.get_json(silent=True)
    if dict_st is None:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get("State", state_id)
    for key, value in dict_st.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
