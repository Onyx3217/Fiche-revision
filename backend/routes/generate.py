from flask import Blueprint, request, jsonify, session
from services.groq_service import generate

generate_bp = Blueprint("generate", __name__, url_prefix="/generate")

@generate_bp.route("/<mode>", methods=["POST"])
def generate_content(mode):
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    text = request.json.get("text")
    result = generate(text, mode)
    return jsonify({"result": result})
