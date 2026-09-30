
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from cloudbox.services import AuthService


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/",
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    auth_service: AuthService = current_app.extensions["auth_service"]
    user = auth_service.authenticate(username, password)

    if user is None:
        return render_template(
            "auth/login.html",
            error="Invalid username or password.",
            username=username,
        ), 401

    session.clear()
    session["user_id"] = user["id"]

    return redirect("/")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    auth_service: AuthService = current_app.extensions["auth_service"]
    user_id = auth_service.create_user(username, password)

    return redirect(url_for("auth.login"))

