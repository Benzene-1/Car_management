from flask import Blueprint
from flask import render_template, request
from website import db
from website.models import User


admin = Blueprint("admin", __name__, template_folder="templates/admin")


@admin.route("/user_management", methods=["GET", "POST"])
def user_management():
    """
    Handles the user management route.

    This function handles both GET and POST requests. For GET requests, it retrieves all users from the database and renders the user management page. 
    For POST requests, it retrieves a specific user's ID from the form, fetches the user from the database, and renders the user management page with the user's data.

    Args:
        None

    Returns:
        render_template("user_management.html", users=users): Renders the user management page with all users for GET requests.
        render_template("user_management.html", user=user): Renders the user management page with a specific user's data for POST requests.
    """

    if request.method == "POST":
        print(request.form)
        user_id = request.form.get("user_id", None)
        print(f"User ID: {user_id}")
        if user_id is not None:
            user = User.query.get(user_id)
            print(f"User: {user}")
            return render_template("user_management.html", user=user)
    else:
        users = User.query.all()
        return render_template("user_management.html", users=users)


@admin.route("/update_user_status/<int:id>", methods=["POST"])
def update_user_status(id):
    """
    Handles the update user status route.

    This function updates the active status of a user based on the form data received in a POST request.

    Args:
        id (int): The user ID that you want to update the status for. This ID is extracted from the URL path when the route is accessed.

    Returns:
        str: A message indicating whether the user status was successfully updated or if the user was not found. 
        If the user is found and the status is updated, it will return a message confirming the update with the new status. 
        If the user is not found in the database, it will return a "User not found" message with a status code of 404.
    """

    print(f"User ID: {id} updating status...")
    print(f"Request args: {request.form}")
    user = User.query.get(id)
    if user:
        new_status = request.form.get("select")
        user.active_status = new_status
        db.session.commit()
        return f"User status updated to {new_status}!"
    else:
        return "User not found", 404
