from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import (
    current_user, login_user, login_required, logout_user  # type: ignore
)
from pydantic import ValidationError
from werkzeug.security import check_password_hash

from src.database.core import session_factory
from src.services import AppointmentService, UserService
from src.utils import flash_pydantic_errors
from src.models import User
from src.schemas import UserCreateSchema, UserLoginSchema


router = Blueprint('auth', __name__)
app = router
current_user: User = current_user


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        try:
            user_schema = UserCreateSchema(**request.form)
        except ValidationError as ex:
            flash_pydantic_errors(ex.errors())
        else:
            with session_factory() as session:
                is_created = UserService(session).add(user_schema.model_dump())
            if is_created:
                return redirect(url_for("auth.login"))
            flash("Пользователь с указанным email уже существует")
    return render_template("auth/signup.html", title="Регистрация")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            user_schema = UserLoginSchema(**request.form)
        except ValidationError as ex:
            flash_pydantic_errors(ex.errors())
        else:
            with session_factory() as session:
                user = UserService(session).get_by_email(user_schema.email)
            if user:
                if check_password_hash(user.password, user_schema.password):
                    if login_user(user, bool(user_schema.remain)):
                        return redirect(url_for("auth.profile"))
            flash("Неверный логин или пароль")
    return render_template("auth/login.html")


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@app.get('/profile')
@login_required
def profile():
    with session_factory() as session:
        appointments = AppointmentService(session).get_by_user(current_user.id)
    return render_template(
        "auth/profile.html", appointments=appointments
    )
