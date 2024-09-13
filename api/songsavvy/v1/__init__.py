# api/songsavvy/v1/__init__.py

# Version-level configurations can be done below

from flask import Blueprint
from ..models import db
import pickle

MODEL_PATH = "api/songsavvy/resources/model.pkl"

songsavvy_v1_blueprint = Blueprint("songsavvy_v1", __name__)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

from .routes import *
