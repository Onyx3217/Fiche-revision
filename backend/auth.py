from flask import Blueprint, request, session, redirect, jsonify
import requests
import os
from urllib.parse import quote_plus
from functools import wraps


auth_bp = Blueprint("auth", __name__)

DISCORD_API = "https://discord.com/api"
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
REQUIRED_ROLE = os.getenv("DISCORD_REQUIRED_ROLE_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("authorized"):
            return jsonify({"error": "Non autorisé"}), 401
        return f(*args, **kwargs)
    return wrapper

@auth_bp.route("/login")
def login():
    return redirect(
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        "&scope=identify"
        f"&redirect_uri={quote_plus(REDIRECT_URI)}"
    )

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "OAuth error", 400

    # Exchange code → token
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
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()

    access_token = token_res.get("access_token")
    if not access_token:
        return "Token invalide", 401

    # User info
    user = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    # Get member via BOT TOKEN (OBLIGATOIRE)
    member = requests.get(
        f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user['id']}",
        headers={"Authorization": f"Bot {BOT_TOKEN}"}
    ).json()

    roles = member.get("roles", [])

    print("ROLES USER :", roles)
    print("ROLE REQUIS :", REQUIRED_ROLE, type(REQUIRED_ROLE))

    if REQUIRED_ROLE not in roles:
        return "⛔ Accès refusé : rôle requis", 403

    # Authorized
    session["authorized"] = True
    session["user_id"] = user["id"]

    return redirect("/revision")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
