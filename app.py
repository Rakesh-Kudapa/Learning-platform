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
import json
import time
from flask import (Flask, request, redirect, url_for, send_from_directory,
                   jsonify, render_template)
from flask_login import login_required, current_user
from dotenv import load_dotenv

from functools import wraps
from models import (db, login_manager, User, Progress, KnowledgeRating,
                    Feedback, Contribution, Doubt, TestResult)

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

    # ------------------------------------------------------------
    #  LLM settings — enter API key from the UI
    # ------------------------------------------------------------
    _settings_path = os.path.join(app.instance_path, "llm_config.json")

    def _load_settings():
        try:
            with open(_settings_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_settings(data):
        with open(_settings_path, "w") as f:
            json.dump(data, f)

    @app.route("/api/settings", methods=["GET"])
    @login_required
    def api_settings_get():
        s = _load_settings()
        provider = s.get("llm_provider", os.getenv("LLM_PROVIDER", "gemini"))
        key = s.get("api_key", "")
        masked = ("" if not key else key[:4] + "•" * max(0, len(key) - 8) + key[-4:])
        return jsonify({
            "llm_provider": provider,
            "api_key_masked": masked,
            "has_key": bool(key),
        })

    @app.route("/api/settings", methods=["POST"])
    @login_required
    def api_settings_post():
        payload = request.get_json(silent=True) or {}
        provider = payload.get("llm_provider", "").strip().lower()
        if provider not in ("gemini", "groq", "ollama"):
            return jsonify({"error": "Provider must be gemini, groq, or ollama"}), 400
        api_key = (payload.get("api_key") or "").strip()
        if provider != "ollama" and not api_key:
            return jsonify({"error": f"API key is required for {provider}"}), 400
        _save_settings({"llm_provider": provider, "api_key": api_key})
        return jsonify({"ok": True})

    # ------------------------------------------------------------
    #  AI doubt tutor  (feat/ask-doubt-tutor)
    # ------------------------------------------------------------
    _ask_cooldowns = {}          # user_id -> last request timestamp
    ASK_COOLDOWN_SECS = 5        # min seconds between requests per user
    ASK_MAX_QUESTION_LEN = 500

    @app.route("/api/ask", methods=["POST"])
    @login_required
    def api_ask():
        now = time.time()
        uid = current_user.id
        last = _ask_cooldowns.get(uid, 0)
        if now - last < ASK_COOLDOWN_SECS:
            return jsonify({"error": "Please wait a few seconds before asking again."}), 429

        payload = request.get_json(silent=True) or {}
        try:
            module_id = int(payload.get("module_id"))
        except (TypeError, ValueError):
            return jsonify({"error": "module_id must be an integer"}), 400

        from course_data import MODULE_TITLES
        if module_id < 0 or module_id >= len(MODULE_TITLES):
            return jsonify({"error": "Invalid module_id"}), 400

        question = (payload.get("question") or "").strip()[:ASK_MAX_QUESTION_LEN]
        if not question:
            return jsonify({"error": "question is required"}), 400

        _ask_cooldowns[uid] = now

        from llm import ask_tutor
        answer = ask_tutor(module_id, question)

        db.session.add(Doubt(
            user_id=uid, module_id=module_id,
            question=question, answer=answer,
        ))
        db.session.commit()

        return jsonify({"answer": answer})

    # ------------------------------------------------------------
    #  Admin dashboard
    # ------------------------------------------------------------
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "").strip().lower()

    def admin_required(f):
        @wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            if current_user.email.lower() != ADMIN_EMAIL:
                return redirect(url_for("course"))
            return f(*args, **kwargs)
        return decorated

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        return render_template("admin.html")

    @app.route("/api/admin/stats")
    @admin_required
    def api_admin_stats():
        from sqlalchemy import func

        users = User.query.order_by(User.created_at).all()

        user_list = []
        for u in users:
            pre = (KnowledgeRating.query
                   .filter_by(user_id=u.id, stage="pre")
                   .order_by(KnowledgeRating.created_at.desc()).first())
            post = (KnowledgeRating.query
                    .filter_by(user_id=u.id, stage="post")
                    .order_by(KnowledgeRating.created_at.desc()).first())
            doubt_count = Doubt.query.filter_by(user_id=u.id).count()
            contrib_count = Contribution.query.filter_by(user_id=u.id).count()
            best_test = (TestResult.query
                         .filter_by(user_id=u.id)
                         .order_by(TestResult.score.desc()).first())
            fb = (Feedback.query.filter_by(user_id=u.id)
                  .order_by(Feedback.created_at.desc()).first())

            user_list.append({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "joined": u.created_at.strftime("%Y-%m-%d %H:%M"),
                "pre_level": pre.level if pre else None,
                "post_level": post.level if post else None,
                "doubts_asked": doubt_count,
                "contributions": contrib_count,
                "best_test_score": f"{best_test.score}/{best_test.total}" if best_test else None,
                "test_passed": best_test.passed if best_test else None,
                "feedback_rating": fb.rating if fb else None,
            })

        reg_dates = {}
        for u in users:
            day = u.created_at.strftime("%Y-%m-%d")
            reg_dates[day] = reg_dates.get(day, 0) + 1

        pre_dist = {"beginner": 0, "medium": 0, "advanced": 0}
        post_dist = {"beginner": 0, "medium": 0, "advanced": 0}
        for u in users:
            pre = (KnowledgeRating.query
                   .filter_by(user_id=u.id, stage="pre")
                   .order_by(KnowledgeRating.created_at.desc()).first())
            post = (KnowledgeRating.query
                    .filter_by(user_id=u.id, stage="post")
                    .order_by(KnowledgeRating.created_at.desc()).first())
            if pre and pre.level in pre_dist:
                pre_dist[pre.level] += 1
            if post and post.level in post_dist:
                post_dist[post.level] += 1

        rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for fb in Feedback.query.all():
            if fb.rating in rating_dist:
                rating_dist[fb.rating] += 1

        from course_data import MODULE_TITLES
        doubts_per_module = []
        for i, title in enumerate(MODULE_TITLES):
            count = Doubt.query.filter_by(module_id=i).count()
            doubts_per_module.append({"module": title, "count": count})

        test_results = TestResult.query.all()
        passed = sum(1 for t in test_results if t.passed)
        failed = len(test_results) - passed

        return jsonify({
            "total_users": len(users),
            "total_doubts": Doubt.query.count(),
            "total_contributions": Contribution.query.count(),
            "total_feedback": Feedback.query.count(),
            "total_tests": len(test_results),
            "users": user_list,
            "registrations_by_date": reg_dates,
            "pre_knowledge": pre_dist,
            "post_knowledge": post_dist,
            "feedback_ratings": rating_dist,
            "doubts_per_module": doubts_per_module,
            "test_pass_fail": {"passed": passed, "failed": failed},
        })

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "rwd-rwe-course"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
