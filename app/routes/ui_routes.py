from flask import Blueprint, render_template


ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/")
def home():
    return render_template("dashboard.html")


@ui_bp.route("/tickets-ui")
def tickets_page():
    return render_template("tickets.html")


@ui_bp.route("/assets-ui")
def assets_page():
    return render_template("assets.html")


@ui_bp.route("/onboarding-ui")
def onboarding_page():
    return render_template("onboarding.html")


@ui_bp.route("/employees-ui")
def employees_page():
    return render_template("employees.html")