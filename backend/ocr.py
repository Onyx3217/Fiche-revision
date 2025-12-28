from flask import Blueprint, request, jsonify
import requests
import os

ocr_bp = Blueprint('ocr', __name__)

OCR_API_URL = "https://api.ocr.space/parse/image"
OCR_API_KEY = os.getenv("OCR_API_KEY")

@ocr_bp.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image'}), 400

    file = request.files['image']

    response = requests.post(
        OCR_API_URL,
        files={"file": file},
        data={
            "apikey": OCR_API_KEY,
            "language": "fre",
            "isOverlayRequired": False
        }
    )

    result = response.json()

    try:
        text = result["ParsedResults"][0]["ParsedText"]
    except (KeyError, IndexError):
        return jsonify({'error': 'OCR échoué'}), 500

    return jsonify({'cours': text})
