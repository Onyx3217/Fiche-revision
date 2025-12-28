from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# Blueprints
from backend.auth import auth_bp
from backend.ai import ai_bp
from backend.ocr import ocr_bp


# =========================
# APP SETUP
# =========================

app = Flask(
    __name__,
    static_folder="../docs",      # frontend
    static_url_path=""            # permet /index.html direct
)

# Secret key (sessions)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")

# Cookies (IMPORTANT pour Discord OAuth)
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("RENDER") is not None
)

# CORS (cookies autorisés)
CORS(app, supports_credentials=True)


# =========================
# BLUEPRINTS (API)
# =========================

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(ai_bp, url_prefix="/api/ai")
app.register_blueprint(ocr_bp, url_prefix="/api/ocr")


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
# DEBUG (OPTIONNEL)
# =========================

print("ENV RENDER :", os.getenv("RENDER"))
print("COOKIE SECURE :", app.config["SESSION_COOKIE_SECURE"])


# =========================
# RUN (LOCAL ONLY)
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
