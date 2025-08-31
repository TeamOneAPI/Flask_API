from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from datetime import datetime
from models import db, Observation

api_bp = Blueprint("api", __name__)

