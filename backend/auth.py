from flask import Blueprint, request, session, redirect
import requests, os, secrets
from urllib.parse import urlencode

auth_bp = Blueprint("auth", __name__)

DISCORD_API = "https://discord.com/api"
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
REQUIRED_ROLE = os.getenv("DISCORD_REQUIRED_ROLE_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

HEADERS = {
    "User-Agent": "fiche-revision-app/1.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

# =========================
# LOGIN
# =========================
@auth_bp.route("/login")
def login():
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": "identify",
        "redirect_uri": REDIRECT_URI,
        "state": state
    }

    return redirect(f"{DISCORD_API}/oauth2/authorize?{urlencode(params)}")

# =========================
# CALLBACK
# =========================
@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or state != session.get("oauth_state"):
        return "OAuth invalide", 400

    session.pop("oauth_state", None)

    token = requests.post(
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

    if token.status_code != 200:
        return "Erreur OAuth Discord", 400

    access_token = token.json().get("access_token")

    user = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    user_id = user.get("id")
    if not user_id:
        return "Utilisateur invalide", 401

    member = requests.get(
        f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}",
        headers={"Authorization": f"Bot {BOT_TOKEN}"}
    )

    if member.status_code != 200:
        return "Non membre du serveur", 403

    roles = member.json().get("roles", [])
    if REQUIRED_ROLE not in roles:
        return "Accès refusé", 403

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
