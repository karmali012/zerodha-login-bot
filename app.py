from flask import Flask, redirect, request, render_template
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

kite = KiteConnect(api_key=API_KEY)

@app.route("/")
def index():
    login_url = kite.login_url()
    return render_template("index.html", login_url=login_url)

@app.route("/callback")
def callback():
    request_token = request.args.get("request_token")
    if not request_token:
        return "❌ No request_token received."
    try:
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        access_token = data["access_token"]
        return f"✅ Access Token Generated:<br><br><code>{access_token}</code><br><br>Copy this and paste into your bot."
    except Exception as e:
        return f"❌ Error: {str(e)}"
