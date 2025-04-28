from flask import Flask, redirect, request, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'somethingsecret'

# Discord app credentials
CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
REDIRECT_URI = "https://randombot-vert.vercel.app/callback"
OAUTH_SCOPE = "identify guilds"

DISCORD_API_BASE = "https://discord.com/api"

@app.route("/")
def home():
    return '<a href="/login">Login with Discord</a>'

@app.route("/login")
def login():
    return redirect(
        f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={OAUTH_SCOPE}"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": OAUTH_SCOPE,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Exchange code for access token
    r = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    tokens = r.json()
    access_token = tokens["access_token"]

    # Use access token to get user info
    userinfo = requests.get(f"{DISCORD_API_BASE}/users/@me", headers={
        "Authorization": f"Bearer {access_token}"
    }).json()

    return f"Hello, {userinfo['username']}! You have successfully logged in."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
