from flask import Blueprint, request, session, redirect, jsonify
import requests, os, secrets
from urllib.parse import quote_plus
from functools import wraps

auth_bp = Blueprint("auth", __name__)

# =========================
# CONFIG
# =========================
DISCORD_API = "https://discord.com/api"
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
REQUIRED_ROLE = os.getenv("DISCORD_REQUIRED_ROLE_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "fiche-revision-app/1.0"
}

# =========================
# DECORATOR
# =========================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("authorized"):
            return jsonify({"error": "Non autorisé"}), 401
        return f(*args, **kwargs)
    return wrapper

# =========================
# LOGIN
# =========================
@auth_bp.route("/login")
def login():
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    return redirect(
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        "&scope=identify"
        f"&redirect_uri={quote_plus(REDIRECT_URI)}"
        f"&state={state}"
    )

# =========================
# CALLBACK
# =========================
@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return "OAuth error", 400

    if state != session.get("oauth_state"):
        return "Invalid OAuth state", 400

    session.pop("oauth_state", None)

    # ---- TOKEN ----
    token_res = requests.post(
        f"{DISCORD_API}/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        headers=HEADERS,
        timeout=10
    )

    if token_res.status_code != 200:
        return "Erreur OAuth Discord", 400

    access_token = token_res.json().get("access_token")
    if not access_token:
        return "Token invalide", 401

    # ---- USER ----
    user = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": HEADERS["User-Agent"]
        },
        timeout=10
    ).json()

    user_id = user.get("id")
    if not user_id:
        return "Utilisateur invalide", 401

    # ---- GUILD MEMBER ----
    member_res = requests.get(
        f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}",
        headers={
            "Authorization": f"Bot {BOT_TOKEN}",
            "User-Agent": HEADERS["User-Agent"]
        },
        timeout=10
    )

    if member_res.status_code != 200:
        return "Accès serveur refusé", 403

    roles = member_res.json().get("roles", [])
    if REQUIRED_ROLE not in roles:
        return "⛔ Rôle requis manquant", 403

    # ---- SESSION OK ----
    session["authorized"] = True
    session["user_id"] = user_id

    return redirect("/revision")

# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
