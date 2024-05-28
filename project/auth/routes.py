from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from project import db
from project.models import User

from . import bp
from .forms import LoginForm, RegisterForm


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Already logged in")
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        try:
            new_user = User(form.username.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash(f"Welcome {new_user.username}!")
            return redirect(url_for("main.home"))
        except IntegrityError:
            db.session.rollback()
            flash("username already exists")
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in")
        return redirect(url_for("main.home"))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.is_password_correct(form.password.data):
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                flash("Welcome Back!")
                return redirect(url_for("main.home"))

        flash("Incorrect credentials")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Goodbye!")
    return redirect(url_for("main.home"))
