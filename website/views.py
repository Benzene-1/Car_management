from flask import Blueprint, redirect, render_template

views = Blueprint("views", __name__, template_folder="templates/regular")


@views.route("/")
def index():
    return redirect("dashboard")
    # return render_template('index.html')


@views.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
