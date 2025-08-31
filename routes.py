from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, Observation
from decorators import role_required  # ✅ claim-based role check

api_bp = Blueprint("api", __name__)

