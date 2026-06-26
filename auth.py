"""
auth.py  —  feat/auth
---------------------
Standard email + password authentication using Flask-Login.
Routes: /register, /login, /logout. Passwords are hashed (never stored raw).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models import db, User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    pw = request.form.get("password", "")

    if not (name and email and pw):
        flash("Please fill in every field.", "error")
        return redirect(url_for("auth.login", mode="register"))
    if len(pw) < 6:
        flash("Password must be at least 6 characters.", "error")
        return redirect(url_for("auth.login", mode="register"))
    if User.query.filter_by(email=email).first():
        flash("That email is already registered — try signing in.", "error")
        return redirect(url_for("auth.login"))

    user = User(name=name, email=email)
    user.set_password(pw)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for("course"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("course"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        pw = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(pw):
            login_user(user)
            nxt = request.args.get("next")
            return redirect(nxt or url_for("course"))
        flash("Wrong email or password.", "error")
        return redirect(url_for("auth.login"))

    mode = request.args.get("mode", "login")   # 'login' | 'register'
    return render_template("login.html", mode=mode)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been signed out.", "ok")
    return redirect(url_for("auth.login"))
