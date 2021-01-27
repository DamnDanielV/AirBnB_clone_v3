#!/usr/bin/python3
"""init file to creates an instance of blueprint"""

from flask import Blueprint

# create a variable app_views which is an instance of Blueprint
# (url prefix must be /api/v1)
app_views = Blueprint("views", __name__, url_prefix="/api/v1")

# wildcard import of everything in the package api.v1.views.index
from api.v1.views.index import *
