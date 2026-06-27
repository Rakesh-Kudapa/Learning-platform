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
from flask import (Flask, request, redirect, url_for, send_from_directory,
                   jsonify, render_template)
from flask_login import login_required, current_user
from dotenv import load_dotenv

from models import db, login_manager, KnowledgeRating, Feedback, Contribution

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

    # ------------------------------------------------------------
    #  Pre/post knowledge self-assessment  (feat/pre-post-feedback-knowledge)
    # ------------------------------------------------------------
    @app.route("/api/assessment", methods=["GET", "POST"])
    @login_required
    def api_assessment():
        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            stage = payload.get("stage")
            level = payload.get("level")
            if stage not in ("pre", "post") or level not in ("beginner", "medium", "advanced"):
                return jsonify({"error": "stage must be pre|post, level must be beginner|medium|advanced"}), 400
            db.session.add(KnowledgeRating(user_id=current_user.id, stage=stage, level=level))
            db.session.commit()
            return jsonify({"ok": True})

        def _latest(stage):
            row = (KnowledgeRating.query
                   .filter_by(user_id=current_user.id, stage=stage)
                   .order_by(KnowledgeRating.created_at.desc()).first())
            return {"level": row.level, "at": row.created_at.isoformat()} if row else None

        return jsonify({"pre": _latest("pre"), "post": _latest("post")})

    # ------------------------------------------------------------
    #  End-of-course feedback  (feat/pre-post-feedback-knowledge)
    # ------------------------------------------------------------
    @app.route("/api/feedback", methods=["POST"])
    @login_required
    def api_feedback():
        payload = request.get_json(silent=True) or {}
        try:
            rating = int(payload.get("rating"))
        except (TypeError, ValueError):
            rating = None
        if rating is None or not (1 <= rating <= 5):
            return jsonify({"error": "rating must be an integer 1-5"}), 400

        db.session.add(Feedback(
            user_id=current_user.id,
            rating=rating,
            experience=(payload.get("experience") or "").strip()[:2000],
            suggestions=(payload.get("suggestions") or "").strip()[:2000],
        ))
        db.session.commit()
        return jsonify({"ok": True})

    # ------------------------------------------------------------
    #  Crowdsourced "extra knowledge" -> Learner Contributions module
    #  (feat/pre-post-feedback-knowledge)
    # ------------------------------------------------------------
    @app.route("/api/contributions", methods=["GET", "POST"])
    @login_required
    def api_contributions():
        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            content = (payload.get("content") or "").strip()
            if not content:
                return jsonify({"error": "content is required"}), 400
            title = (payload.get("title") or "").strip()[:140] or "A tip from a fellow learner"
            db.session.add(Contribution(
                user_id=current_user.id, title=title,
                content=content[:4000], status="approved"))
            db.session.commit()
            return jsonify({"ok": True})

        rows = (Contribution.query.filter_by(status="approved")
                .order_by(Contribution.created_at.desc()).all())
        return jsonify([
            {"author_name": r.user.name, "title": r.title, "content": r.content,
             "created_at": r.created_at.strftime("%d %b %Y")}
            for r in rows
        ])

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "rwd-rwe-course"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
