from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, Observation
from decorators import role_required  # ✅ claim-based role check

api_bp = Blueprint("api", __name__)

# Utility: check if record is editable (US-11)
def is_current_quarter(date_str):
    record_date = datetime.strptime(date_str, "%Y-%m-%d")
    now = datetime.utcnow()
    quarter_start = datetime(now.year, (now.month - 1) // 3 * 3 + 1, 1)
    return record_date >= quarter_start
