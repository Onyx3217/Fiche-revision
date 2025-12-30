from flask import Blueprint, request, jsonify, session
from services.ocr_service import extract_text
from auth.permissions import api_login_required

ocr_bp = Blueprint("ocr", __name__, url_prefix="/ocr")

@ocr_bp.route("/upload", methods=["POST"])
@api_login_required
def upload():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files["file"]
    text = extract_text(file)
    return jsonify({"text": text})


