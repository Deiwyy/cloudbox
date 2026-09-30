from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash

explorer_bp = Blueprint("explorer", __name__, url_prefix="/")


@explorer_bp.route("/", methods=["GET"])
def index():
    return render_template("explorer/index.html")