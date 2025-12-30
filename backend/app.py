from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.auth import auth_bp
from backend.ai import ai_bp
from backend.ocr import ocr_bp

app = Flask(
    __name__,
    static_folder="../docs",
    static_url_path=""
)

# =========================
# CONFIG
# =========================
app.secret_key = os.getenv("SECRET_KEY")

IS_RENDER = os.getenv("RENDER") == "true"

app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=IS_RENDER
)

CORS(app, supports_credentials=True)

# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(ai_bp, url_prefix="/api/ai")
app.register_blueprint(ocr_bp, url_prefix="/api/ocr")

# =========================
# ROUTES FRONT
# =========================
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/revision")
def revision():
    return send_from_directory(app.static_folder, "revision.html")

@app.route("/health")
def health():
    return "OK"
