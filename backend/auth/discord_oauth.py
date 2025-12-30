from flask import Blueprint, redirect, request, session
import requests, os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
DISCORD_API = "https://discord.com/api"

@auth_bp.route("/login")
def login():
    return redirect(
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={os.getenv('DISCORD_CLIENT_ID')}"
        "&response_type=code"
        "&scope=identify guilds.members.read"
        f"&redirect_uri={os.getenv('DISCORD_REDIRECT_URI')}"
    )

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")

    token = requests.post(f"{DISCORD_API}/oauth2/token", data={
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI")
    }).json()

    headers = {"Authorization": f"Bearer {token['access_token']}"}

    user = requests.get(f"{DISCORD_API}/users/@me", headers=headers).json()
    member = requests.get(
        f"{DISCORD_API}/users/@me/guilds/{os.getenv('DISCORD_GUILD_ID')}/member",
        headers=headers
    ).json()

    if os.getenv("DISCORD_REQUIRED_ROLE_ID") not in member.get("roles", []):
        return "Accès refusé", 403

    session["user"] = {
        "id": user["id"],
        "username": user["username"],
        "avatar": user["avatar"]
    }

    return redirect("/dashboard")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
