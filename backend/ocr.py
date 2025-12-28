# filepath: c:\Users\Champeley\Desktop\Fiche de révision\backend\ocr.py
from flask import Blueprint, request, jsonify
import pytesseract
from PIL import Image
import io

# Spécifiez le chemin vers tesseract.exe (ajustez si nécessaire)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image'}), 400

    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    text = pytesseract.image_to_string(image, lang='fra')
    return jsonify({'cours': text})