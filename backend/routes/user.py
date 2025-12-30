from flask import Blueprint, jsonify, session
from auth.permissions import api_login_required

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/me")
@api_login_required
def me():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(session["user"])
