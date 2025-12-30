from flask import Flask, render_template, session, redirect
from config import Config

from auth.discord_oauth import auth_bp
from routes.generate import generate_bp
from routes.ocr import ocr_bp
from routes.user import user_bp
from auth.permissions import login_required

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(generate_bp)
app.register_blueprint(ocr_bp)
app.register_blueprint(user_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", user=session["user"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
