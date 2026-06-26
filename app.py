"""
app.py — Excelra RWD/RWE Learning Platform
==========================================
Application factory. Wires config, the database, Flask-Login, and the auth
blueprint, then exposes the login-protected course.

Branches so far:
  feat/auth  (this) -> register / login / logout + course behind a login wall

Run:
    flask --app app run --debug      (or)      python app.py
    -> http://localhost:5000
"""
import os
from flask import (Flask, redirect, url_for, send_from_directory,
                   jsonify, render_template)
from flask_login import login_required, current_user
from dotenv import load_dotenv

from models import db, login_manager

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # --- config ---
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, "course.db")
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-change-me"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # --- extensions ---
    db.init_app(app)
    login_manager.init_app(app)

    # --- blueprints ---
    from auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    # --- routes ---
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("course"))
        return redirect(url_for("auth.login"))

    @app.route("/course")
    @login_required
    def course():
        # served as a static file (no Jinja) — it's a self-contained app
        return send_from_directory(
            os.path.join(app.root_path, "templates"), "course.html")

    @app.route("/api/me")
    @login_required
    def api_me():
        return jsonify({"name": current_user.name, "email": current_user.email})

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "rwd-rwe-course"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
