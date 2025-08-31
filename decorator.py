from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_required(required_role):
    """
    Restrict access to users with a specific role.
    Example: @role_required("admin")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Make sure a JWT is present and valid
            verify_jwt_in_request()

            # ✅ Extract claims (we stored role in login as additional_claims)
            claims = get_jwt()

            # If role mismatch, block access
            if claims.get("role") != required_role:
                return jsonify({"error": "Forbidden: insufficient permissions"}), 403

            # Otherwise, continue to the route
            return fn(*args, **kwargs)
        return wrapper
    return decorator
