from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash

from cloudbox.services.auth import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/")


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        auth: AuthService = current_app.extensions["auth"]         

        user = auth.authenticate_user(username, password)

        if user:
            flash("Login successful!", "success")
            return redirect("/")
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login", error="invalid"))

    error = request.args.get("error")

    return render_template("auth/login.html", error=error)

    return "Login Page", 200