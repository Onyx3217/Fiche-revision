from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, send_from_directory
from flask_cors import CORS
import os

from backend.auth import auth_bp
from backend.ai import ai_bp
from backend.ocr import ocr_bp


app = Flask(
    __name__,
    static_folder="../docs",
    static_url_path=""
)


app.secret_key = os.getenv("SECRET_KEY", "default_secret")

app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)

CORS(app, supports_credentials=True)

# Blueprints API
app.register_blueprint(auth_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(ocr_bp)

# =========================
# FRONTEND ROUTES
# =========================

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/revision")
def revision():
    return send_from_directory(app.static_folder, "revision.html")

@app.route("/services")
def services():
    return send_from_directory(app.static_folder, "services.html")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run()
