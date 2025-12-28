from flask import Blueprint, request, session, redirect, jsonify
import requests
import os
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

DISCORD_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    # ⚠️ OBLIGATOIRE pour éviter Cloudflare 1015
    "User-Agent": "fiche-revision-app/1.0 (contact: theo)"
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
    return redirect(
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        "&scope=identify"
        f"&redirect_uri={quote_plus(REDIRECT_URI)}"
    )

# =========================
# CALLBACK
# =========================
@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "OAuth error: no code", 400

    # ---- Exchange code → token ----
    token_res = requests.post(
        f"{DISCORD_API}/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "scope": "identify"
        },
        headers=DISCORD_HEADERS,
        timeout=10
    )

    # 🔥 LOGS CRUCIAUX
    print("TOKEN STATUS:", token_res.status_code)
    print("TOKEN TEXT:", token_res.text)

    if token_res.status_code != 200:
        return "Erreur OAuth Discord", 400

    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return "Token invalide", 401

    # ---- Get user info ----
    user_res = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": DISCORD_HEADERS["User-Agent"]
        },
        timeout=10
    )

    user = user_res.json()
    user_id = user.get("id")

    if not user_id:
        return "Utilisateur Discord invalide", 401

    # ---- Get guild member (BOT TOKEN) ----
    member_res = requests.get(
        f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}",
        headers={
            "Authorization": f"Bot {BOT_TOKEN}",
            "User-Agent": DISCORD_HEADERS["User-Agent"]
        },
        timeout=10
    )

    if member_res.status_code != 200:
        return "Impossible de vérifier le serveur Discord", 403

    member = member_res.json()
    roles = member.get("roles", [])

    print("ROLES USER:", roles)
    print("ROLE REQUIS:", REQUIRED_ROLE)

    if REQUIRED_ROLE not in roles:
        return "⛔ Accès refusé : rôle requis", 403

    # ---- Session OK ----
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
