from application import db

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm


@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form=RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/registerform.html", form=form)

    existing = User.query.filter_by(username=form.username.data).first()

    if existing is not None:
        return render_template("auth/registerform.html", form=form,
                               error="Username already exists")

    user = User(username=form.username.data,
                plaintext=form.password.data,
                admin=form.admin.data)

    db.session().add(user)
    db.session().commit()

    return redirect(url_for("auth_login"))


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/loginform.html", form=LoginForm())

    user = User.query.filter_by(username=form.username.data).first()

    if not user or not user.is_correct_password(form.password.data):
        return render_template("auth/loginform.html", form=form,
                               error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("auth_login"))
