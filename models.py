"""
models.py
---------
The database schema for the whole project, defined once up front so every
later feature branch (auth, assessment, doubts, test, feedback, contributions)
plugs into a stable shape. SQLite for now; swap SQLALCHEMY_DATABASE_URI to
Postgres later with no model changes.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """A learner account."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    # relationships
    progress = db.relationship("Progress", backref="user", uselist=False, cascade="all, delete-orphan")
    ratings = db.relationship("KnowledgeRating", backref="user", cascade="all, delete-orphan")
    doubts = db.relationship("Doubt", backref="user", cascade="all, delete-orphan")
    results = db.relationship("TestResult", backref="user", cascade="all, delete-orphan")
    feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")
    contributions = db.relationship("Contribution", backref="user", cascade="all, delete-orphan")
    module_unlocks = db.relationship("ModuleUnlock", backref="user", cascade="all, delete-orphan")
    exam_unlock = db.relationship("ExamUnlock", backref="user", uselist=False, cascade="all, delete-orphan")


class Progress(db.Model):
    """Per-user course state (xp, completed modules, badges) as JSON text."""
    __tablename__ = "progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    data = db.Column(db.Text, default="{}")          # json blob
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KnowledgeRating(db.Model):
    """Self-rated knowledge level — captured BEFORE and AFTER the course."""
    __tablename__ = "knowledge_ratings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stage = db.Column(db.String(10), nullable=False)   # 'pre' | 'post'
    level = db.Column(db.String(12), nullable=False)    # 'beginner' | 'medium' | 'advanced'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Doubt(db.Model):
    """A question a learner asked the AI tutor inside a module, plus the answer."""
    __tablename__ = "doubts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TestResult(db.Model):
    """A whole-course final test attempt. Certificate unlocks when passed."""
    __tablename__ = "test_results"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    """End-of-course experience, rating, and suggested changes."""
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rating = db.Column(db.Integer)                     # 1-5 stars
    experience = db.Column(db.Text)                    # "how did you find it?"
    suggestions = db.Column(db.Text)                   # "changes we should make"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Contribution(db.Model):
    """Extra knowledge a learner adds that isn't in the course.
    Auto-surfaced in the 'Learners' Extra Knowledge' module for future users."""
    __tablename__ = "contributions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(12), default="approved")  # 'approved' | 'pending' (optional moderation)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminGrant(db.Model):
    """An email granted admin access by the primary admin (ADMIN_EMAIL in
    .env). The primary admin itself is never stored here — it's always
    derived from the env var, so it can never be locked out via the UI."""
    __tablename__ = "admin_grants"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    granted_by = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ModuleUnlock(db.Model):
    """An admin override that force-unlocks one module for one user,
    bypassing the normal sequential knowledge-check gate."""
    __tablename__ = "module_unlocks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("user_id", "module_id", name="uq_user_module"),)


class ExamUnlock(db.Model):
    """Admin override that gives one user access to the final exam
    regardless of whether they've completed all module knowledge checks."""
    __tablename__ = "exam_unlocks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ------------------------------------------------------------------
#  Auth plumbing (Flask-Login). Kept here so the User model and its
#  loader live together and there is no circular import.
# ------------------------------------------------------------------
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
