#!/usr/bin/python3
"""first endpoint (route)"""

from os import environ
from flask import Flask, Blueprint, jsonify

from api.v1.views import app_views
from models import storage

# create a variable app, instance of Flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views, url="/app_views")


# declare a method to handle @app.teardown_appcontext that calls storage.close
@app.teardown_appcontext
def tear(exception):
    """calls storage.close"""
    storage.close()


# create a handler for 404 errors that returns a JSON-formatted
# 404 status code response. The content should be: "error": "Not found"
@app.errorhandler(404)
def error_han(e):
    """ 404 errors that returns a JSON """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.register_error_handler(404, error_han)
    app.run(
        host=host,
        port=port,
        threaded=True)
