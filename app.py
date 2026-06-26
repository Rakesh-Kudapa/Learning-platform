"""
app.py  —  Step 1 scaffold
--------------------------
A minimal but RUNNABLE Flask app using the application-factory pattern.
It loads config, initialises the database (creating all tables from models.py),
and serves a status landing page so you can confirm the stack works end to end
before any feature branches are layered on.

Run it:
    flask --app app run --debug
or:
    python app.py
"""
import os
from flask import Flask, render_template
from dotenv import load_dotenv

from models import db

load_dotenv()  # read .env


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
    with app.app_context():
        db.create_all()  # creates all tables defined in models.py

    # --- routes (Step 1: just a status page; features arrive on later branches) ---
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "rwd-rwe-course"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
