from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, ProfileForm, RegistrationForm
from app.models import User

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        if db.session.scalar(db.select(User).where(User.username == username)):
            flash("Username is already registered.", "danger")
            return render_template("auth/register.html", form=form)
        if db.session.scalar(db.select(User).where(User.email == email)):
            flash("Email is already registered.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(username=username, email=email)
        user.set_password(form.password.data)
        user.is_admin = db.session.scalar(db.select(User.id).limit(1)) is None
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.username == form.username.data.strip()))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html", form=form)
        login_user(user)
        flash("Welcome back!", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))

@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data.strip()
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("auth.profile"))
    return render_template("auth/profile.html", form=form, user=current_user)
