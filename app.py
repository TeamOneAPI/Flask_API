from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint("auth", __name__)

# 🔹 Register new user
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  # 👈 default role = "user"

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "role": role}), 201


# 🔹 Login existing user
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # ✅ identity must be a string (username)
        # ✅ role is stored in additional_claims
        token = create_access_token(
            identity=username,
            additional_claims={"role": user.role}
        )
        return jsonify(access_token=token), 200

    return jsonify({"error": "Invalid credentials"}), 401
