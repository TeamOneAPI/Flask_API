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


# ✅ Create observation (User + Admin)
@api_bp.route("/observations", methods=["POST"])
@jwt_required()
def create_observation():
    data = request.json
    obs = Observation(**data)
    db.session.add(obs)
    db.session.commit()
    return jsonify({"message": "Observation created", "id": obs.id}), 201

# ✅ Bulk create (User + Admin)
@api_bp.route("/observations/bulk", methods=["POST"])
@jwt_required()
def bulk_create_observations():
    data_list = request.json.get("records", [])
    results = []
    for data in data_list:
        obs = Observation(**data)
        db.session.add(obs)
        db.session.flush()  # 👈 ensures obs.id is populated before commit
        results.append({"id": obs.id, "status": "created"})
    db.session.commit()
    return jsonify(results), 200


# ✅ Bulk update (Admin only)
@api_bp.route("/observations/bulk", methods=["PUT"])
@jwt_required()
@role_required("admin")
def bulk_update_observations():
    data_list = request.json.get("records", [])
    results = []
    for data in data_list:
        obs = Observation.query.get(data["id"])
        if obs:
            for k, v in data.items():
                if k != "id":
                    setattr(obs, k, v)
            results.append({"id": obs.id, "status": "updated"})
        else:
            results.append({"id": data["id"], "status": "not found"})
    db.session.commit()
    return jsonify(results), 200