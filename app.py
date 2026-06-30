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
                    Feedback, Contribution, Doubt, TestResult,
                    AdminGrant, ModuleUnlock)

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # --- config ---
    os.makedirs(app.instance_path, exist_ok=True)
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
    else:
        db_path = os.path.join(app.instance_path, "course.db")
        database_url = f"sqlite:///{db_path}"
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-change-me"),
        SQLALCHEMY_DATABASE_URI=database_url,
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

    # --- mode ---
    APP_MODE = os.getenv("APP_MODE", "full").strip().lower()
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "").strip().lower()

    def is_super_admin():
        return current_user.is_authenticated and current_user.email.lower() == ADMIN_EMAIL

    def is_admin_user():
        if not current_user.is_authenticated:
            return False
        email = current_user.email.lower()
        if email == ADMIN_EMAIL:
            return True
        return AdminGrant.query.filter_by(email=email).first() is not None

    # --- routes ---
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if APP_MODE == "admin" and not is_admin_user():
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("course"))
        return redirect(url_for("auth.login"))

    @app.route("/course")
    @login_required
    def course():
        # The admin account always has full access to the learning tool,
        # on either deployment. Only non-admins get redirected on the
        # admin-only deployment.
        if APP_MODE == "admin" and not is_admin_user():
            return redirect(url_for("admin_dashboard"))
        return send_from_directory(
            os.path.join(app.root_path, "templates"), "course.html")

    @app.route("/api/me")
    @login_required
    def api_me():
        unlocks = ModuleUnlock.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            "name": current_user.name,
            "email": current_user.email,
            "is_admin": is_admin_user(),
            "unlocked_modules": [u.module_id for u in unlocks],
        })

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
        if provider not in ("gemini", "groq"):
            return jsonify({"error": "Provider must be gemini or groq"}), 400
        api_key = (payload.get("api_key") or "").strip()
        if not api_key:
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
    #  Final test & certificate  (feat/final-test-certificate)
    # ------------------------------------------------------------
    @app.route("/api/test", methods=["GET"])
    @login_required
    def api_test():
        from course_data import TEST_QUESTIONS
        return jsonify([
            {"id": i, "q": q["q"], "options": q["options"]}
            for i, q in enumerate(TEST_QUESTIONS)
        ])

    @app.route("/api/test/submit", methods=["POST"])
    @login_required
    def api_test_submit():
        from course_data import TEST_QUESTIONS, PASS_MARK
        payload = request.get_json(silent=True) or {}
        answers = payload.get("answers") or {}
        if not isinstance(answers, dict):
            return jsonify({"error": "answers must be an object of {questionId: optionIndex}"}), 400

        total = len(TEST_QUESTIONS)
        score = 0
        for i, q in enumerate(TEST_QUESTIONS):
            given = answers.get(str(i))
            if isinstance(given, int) and given == q["answer"]:
                score += 1

        passed = (score / total) >= PASS_MARK if total else False

        db.session.add(TestResult(
            user_id=current_user.id, score=score, total=total, passed=passed,
        ))
        db.session.commit()

        return jsonify({"score": score, "total": total, "passed": passed,
                        "pass_mark": PASS_MARK})

    @app.route("/api/test/results", methods=["GET"])
    @login_required
    def api_test_results():
        from course_data import PASS_MARK
        rows = (TestResult.query.filter_by(user_id=current_user.id)
                .order_by(TestResult.created_at.desc()).all())
        best = max(rows, key=lambda r: r.score, default=None)
        return jsonify({
            "attempts": [
                {"score": r.score, "total": r.total, "passed": r.passed,
                 "at": r.created_at.isoformat()}
                for r in rows
            ],
            "best": ({"score": best.score, "total": best.total, "passed": best.passed,
                     "at": best.created_at.isoformat()} if best else None),
            "pass_mark": PASS_MARK,
        })

    # ------------------------------------------------------------
    #  Admin dashboard — rakeshkudapa01@gmail.com (ADMIN_EMAIL) has full,
    #  unrestricted access to both the admin portal and the learning tool,
    #  on every deployment, regardless of APP_MODE.
    # ------------------------------------------------------------
    def admin_required(f):
        @wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            if not is_admin_user():
                if APP_MODE == "admin":
                    return redirect(url_for("auth.login"))
                return redirect(url_for("course"))
            return f(*args, **kwargs)
        return decorated

    def super_admin_required(f):
        # Granting/revoking admin access is restricted to the primary admin
        # (ADMIN_EMAIL) only — DB-granted admins can't create or remove
        # further admins, to prevent an uncontrolled privilege chain.
        @wraps(f)
        @admin_required
        def decorated(*args, **kwargs):
            if not is_super_admin():
                return jsonify({"error": "Only the primary admin can manage admin access"}), 403
            return f(*args, **kwargs)
        return decorated

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        return render_template("admin.html")

    # ------------------------------------------------------------
    #  Admin access management — grant/revoke/list admins
    # ------------------------------------------------------------
    @app.route("/api/admin/admins", methods=["GET"])
    @admin_required
    def api_admin_admins_list():
        grants = AdminGrant.query.order_by(AdminGrant.created_at).all()
        return jsonify({
            "super_admin": ADMIN_EMAIL,
            "is_super_admin": is_super_admin(),
            "granted": [
                {"email": g.email, "granted_by": g.granted_by,
                 "created_at": g.created_at.strftime("%Y-%m-%d %H:%M")}
                for g in grants
            ],
        })

    @app.route("/api/admin/admins", methods=["POST"])
    @super_admin_required
    def api_admin_admins_grant():
        payload = request.get_json(silent=True) or {}
        email = (payload.get("email") or "").strip().lower()
        if not email or "@" not in email:
            return jsonify({"error": "A valid email is required"}), 400
        if email == ADMIN_EMAIL:
            return jsonify({"error": "That email is already the primary admin"}), 400
        if AdminGrant.query.filter_by(email=email).first():
            return jsonify({"error": "That email already has admin access"}), 400
        db.session.add(AdminGrant(email=email, granted_by=current_user.email))
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/admin/admins/revoke", methods=["POST"])
    @super_admin_required
    def api_admin_admins_revoke():
        payload = request.get_json(silent=True) or {}
        email = (payload.get("email") or "").strip().lower()
        if email == ADMIN_EMAIL:
            return jsonify({"error": "The primary admin can't be revoked from the portal"}), 400
        grant = AdminGrant.query.filter_by(email=email).first()
        if not grant:
            return jsonify({"error": "That email doesn't have granted admin access"}), 404
        db.session.delete(grant)
        db.session.commit()
        return jsonify({"ok": True})

    # ------------------------------------------------------------
    #  Per-user module unlock overrides — bypass the sequential gate
    # ------------------------------------------------------------
    def _valid_module_id(payload):
        try:
            mid = int(payload.get("module_id"))
        except (TypeError, ValueError):
            return None
        from course_data import MODULE_TITLES
        if mid < 0 or mid >= len(MODULE_TITLES):
            return None
        return mid

    @app.route("/api/admin/unlock", methods=["POST"])
    @admin_required
    def api_admin_unlock():
        payload = request.get_json(silent=True) or {}
        user = db.session.get(User, payload.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 404
        mid = _valid_module_id(payload)
        if mid is None:
            return jsonify({"error": "Invalid module_id"}), 400
        if not ModuleUnlock.query.filter_by(user_id=user.id, module_id=mid).first():
            db.session.add(ModuleUnlock(user_id=user.id, module_id=mid))
            db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/admin/lock", methods=["POST"])
    @admin_required
    def api_admin_lock():
        payload = request.get_json(silent=True) or {}
        user = db.session.get(User, payload.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 404
        mid = _valid_module_id(payload)
        if mid is None:
            return jsonify({"error": "Invalid module_id"}), 400
        ModuleUnlock.query.filter_by(user_id=user.id, module_id=mid).delete()
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/admin/unlock-all", methods=["POST"])
    @admin_required
    def api_admin_unlock_all():
        from course_data import MODULE_TITLES
        payload = request.get_json(silent=True) or {}
        user = db.session.get(User, payload.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 404
        existing = {u.module_id for u in ModuleUnlock.query.filter_by(user_id=user.id).all()}
        for mid in range(len(MODULE_TITLES)):
            if mid not in existing:
                db.session.add(ModuleUnlock(user_id=user.id, module_id=mid))
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/admin/lock-all", methods=["POST"])
    @admin_required
    def api_admin_lock_all():
        payload = request.get_json(silent=True) or {}
        user = db.session.get(User, payload.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 404
        ModuleUnlock.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/admin/answer-key")
    @admin_required
    def api_admin_answer_key():
        from course_data import MODULE_QUIZZES, MODULE_TITLES, TEST_QUESTIONS
        modules = []
        for i, title in enumerate(MODULE_TITLES):
            modules.append({
                "id": i,
                "title": title,
                "questions": MODULE_QUIZZES.get(i, []),
            })
        return jsonify({
            "modules": modules,
            "final_exam": TEST_QUESTIONS,
        })

    @app.route("/api/admin/reset", methods=["POST"])
    @admin_required
    def api_admin_reset():
        # Wipes learner data only. AdminGrant (admin role assignments) is
        # intentionally preserved — wiping test users shouldn't strip
        # anyone's admin access.
        Contribution.query.delete()
        Feedback.query.delete()
        TestResult.query.delete()
        Doubt.query.delete()
        KnowledgeRating.query.delete()
        ModuleUnlock.query.delete()
        Progress.query.delete()
        User.query.delete()
        db.session.commit()
        return jsonify({"ok": True, "message": "All data cleared"})

    @app.route("/api/admin/stats")
    @admin_required
    def api_admin_stats():
        from sqlalchemy import func
        from course_data import MODULE_TITLES

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
            unlocked = [m.module_id for m in ModuleUnlock.query.filter_by(user_id=u.id).all()]

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
                "unlocked_modules": unlocked,
                "is_admin": (u.email.lower() == ADMIN_EMAIL or
                             AdminGrant.query.filter_by(email=u.email.lower()).first() is not None),
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

        doubts_per_module = []
        for i, title in enumerate(MODULE_TITLES):
            count = Doubt.query.filter_by(module_id=i).count()
            doubts_per_module.append({"module": title, "count": count})

        test_results = TestResult.query.all()
        passed = sum(1 for t in test_results if t.passed)
        failed = len(test_results) - passed

        recent_doubts = (Doubt.query.order_by(Doubt.created_at.desc())
                         .limit(200).all())
        doubt_list = []
        for d in recent_doubts:
            doubt_list.append({
                "user": d.user.name,
                "module": MODULE_TITLES[d.module_id] if d.module_id < len(MODULE_TITLES) else f"Module {d.module_id}",
                "question": d.question,
                "date": d.created_at.strftime("%Y-%m-%d %H:%M"),
            })

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
            "recent_doubts": doubt_list,
        })

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "rwd-rwe-course"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
