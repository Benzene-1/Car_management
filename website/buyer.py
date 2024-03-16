from flask import Blueprint, render_template, request
from flask_login import current_user

from website import db
from website.models import CarComponent, CarRequest

buyer = Blueprint("buyer", __name__, template_folder="templates/buyer")


@buyer.route("/request-car", methods=["GET", "POST"])
def request_car():
    """
    Handles the request car route.

    This function handles both GET and POST requests. If the request method is POST, it retrieves the form data, 
    creates a new CarRequest instance with the form data and the current user's ID, 
    adds the new CarRequest instance to the database, and commits the changes. 
    Regardless of the request method, it then renders the 'request_car_import.html' template.

    Args:
        None

    Returns:
        str: The rendered 'request_car_import.html' template.
    """

    if request.method == "POST":
        print(request.form)
        title = request.form.get("title")
        make = request.form.get("make")
        model = request.form.get("model")
        year = request.form.get("year")
        color = request.form.get("color")
        details = request.form.get("details")

        car_request = CarRequest(
            title=title,
            make=make,
            model=model,
            year=year,
            color=color,
            details=details,
            user_id=current_user.id,
        )
        db.session.add(car_request)
        db.session.commit()

    return render_template("request_car_import.html")

@buyer.route("/request_car_parts", methods=["GET", "POST"])
def request_car_parts():
    print(request.form)

    if len(request.form) != 0:
        new_component_request = CarComponent(
            component_name=request.form.get("component_name"),
            manufacturer=request.form.get("manufacturer"),
            details=request.form.get("details"),
            quantity=request.form.get("quantity"),
            user_id=current_user.id,
        )

        db.session.add(new_component_request)
        db.session.commit()
        print("New component request added successfully!")

    return render_template("request_car_parts.html")


@buyer.route("/my-invoices", methods=["GET", "POST"])
def my_invoices():
    """
    Handles the my invoices route.

    This function retrieves all Invoice instances associated with the current user's ID from the database, 
    and then renders the 'my_invoices.html' template with these Invoice instances.

    Args:
        None

    Returns:
        str: The rendered 'my_invoices.html' template with all Invoice instances associated with the current user's ID.
    """

    # my_invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    # print(my_invoices)

    return render_template("my_invoices.html", my_invoices=my_invoices)

@buyer.route("/my-component-requests", methods=["GET", "POST"])
def my_component_requests():
    """
    Handles the my component requests route.

    This function retrieves all CarComponent instances associated with the current user's ID from the database, 
    and then renders the 'my_component_requests.html' template with these CarComponent instances.

    Args:
        None

    Returns:
        str: The rendered 'my_component_requests.html' template with all CarComponent instances associated with the current user's ID.
    """

    my_components = CarComponent.query.filter_by(user_id=current_user.id).all()
    print(my_components)

    return render_template("my_component_requests.html", my_components=my_components)