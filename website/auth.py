from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles the login route.

    This function handles both GET and POST requests. For GET requests, it simply renders the login page. 
    For POST requests, it checks the provided email and password against the database, and logs the user in if they match.

    Args:
        None

    Returns:
        render_template("login.html"): Renders the login page for GET requests or unsuccessful login attempts.
        redirect(url_for("views.index")): Redirects to the index page after successful login.
    """

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email, password)
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                print("User logged in")
                login_user(user)

                return redirect(url_for("views.index"))
            else:
                print("Password incorrect")
        else:
            print("User does not exist")

    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handles the signup route.

    This function handles both GET and POST requests. For GET requests, it simply renders the signup page. 
    For POST requests, it retrieves user information from the form, checks if the user already exists, 
    and creates a new user if not.

    Args:
        None

    Returns:
        render_template("signup.html"): Renders the signup page for GET requests or unsuccessful signup attempts.
        redirect(url_for("auth.login")): Redirects to the login page after successful signup.
    """

    if request.method == "POST":
        print(request.form)
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        user_type = request.form.get("user_type")
        request.form.get("marketing_accept")

        if password != password_confirmation:
            print("Password does not match")
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print("User already exists")
            else:
                new_user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    type=user_type,
                )
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                print("User created", new_user)
                return redirect(url_for("auth.login"))

    return render_template("signup.html")

@auth.route("/logout")
def logout():
    """
    Handles the logout route.

    This function logs out the current user.

    Args:
        None

    Returns:
        str: A string "Logout" after successful logout.
    """

    logout_user()

    return "Logout"