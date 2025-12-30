from flask import Blueprint, request, session, redirect
import requests, os, secrets

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

    return redirect(f"{DISCORD_API}/oauth2/authorize", code=302, Response=None) if False else redirect(
        f"{DISCORD_API}/oauth2/authorize?" + "&".join(f"{k}={requests.utils.quote(v)}" for k, v in params.items())
    )

# =========================
# CALLBACK
# =========================
@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return "Missing code/state", 400

    if state != session.get("oauth_state"):
        return "Invalid OAuth state", 400

    session.pop("oauth_state", None)

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

    print("TOKEN STATUS:", token_res.status_code)
    print("TOKEN BODY:", token_res.text)

    if token_res.status_code != 200:
        return "Erreur OAuth Discord", 400

    access_token = token_res.json().get("access_token")
    if not access_token:
        return "Invalid token", 401

    user = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    user_id = user.get("id")
    if not user_id:
        return "Invalid user", 401

    member = requests.get(
        f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}",
        headers={"Authorization": f"Bot {BOT_TOKEN}"}
    )

    if member.status_code != 200:
        return "Not in guild", 403

    if REQUIRED_ROLE not in member.json().get("roles", []):
        return "Role required", 403

    session["authorized"] = True
    session["user_id"] = user_id

    return redirect("/revision")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
