from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from . import db
from .models import Car, CarComponent, Card, User

seller = Blueprint("seller", __name__, template_folder="templates/seller")


@seller.route("/bidding-payment", methods=["GET", "POST"])
def bidding_payment():
    """
    Handles the bidding payment route.

    This function handles both GET and POST requests. If the request method is POST, it retrieves the form data,
    validates the card details, and if valid, processes the payment, updates the user's balance and spent amount,
    updates the car's status and owner, and redirects to the 'my_invoices' route. If the card details are not valid,
    it prints an error message. Regardless of the request method, it then calculates a discount based on the user's spent amount,
    calculates the final amount, and renders the 'bidding_payment.html' template with these details.

    Args:
        None

    Returns:
        str: The rendered 'bidding_payment.html' template with the car ID, new bid, user ID, user discount, and final amount.
    """

    if request.method == "POST":
        print(request.form)
        card_number = request.form.get("card_number", None)
        expiry = request.form.get("expiry", None)
        cvv = request.form.get("cvv", None)
        print(f"Card: {card_number}, Expiry: {expiry}, CVV: {cvv}")
        if card_number and expiry and cvv:
            print("Processing payment...")
            is_valid_card = Card.query.filter_by(card_number=card_number).first()
            if is_valid_card:
                if all([is_valid_card.expiry_date == expiry, is_valid_card.cvv == cvv]):
                    car_id = session.get("car_id", None)
                    new_bid = session.get("new_bid", None)
                    user_id = session.get("user_id", None)
                    print("Card Info Matched...")
                    print(f"Debiting {new_bid} from {current_user}")

                    user = User.query.get(current_user.id)
                    balance = int(user.balance)
                    new_balance = balance - int(new_bid)
                    user.balance = new_balance

                    spent_amount = int(user.spent_amount)
                    user.spent_amount = spent_amount + int(new_bid)

                    db.session.commit()
                    print("Payment successful...")

                    car = Car.query.get(car_id)
                    car.status = "BidBooked"
                    print(f"Car status updated to BidBooked... {car}")
                    car.user_id = user_id
                    print(f"Car user_id updated to {user_id}... {car}")
                    
                    db.session.commit()
                    print("Car status updated to BidBooked...")

                    # Clear the session variables
                    session["car_id"] = None
                    session["new_bid"] = None
                    session["user_id"] = None
                
                    return redirect(url_for("seller.my_invoices"))
                else:
                    print("Card Info Mismatch")
            else:
                print("Invalid payment details")

        else:
            print("Invalid payment details")
    car_id = session.get("car_id", None)
    new_bid = session.get("new_bid", None)
    user_id = session.get("user_id", None)

    # calculate a discount based on the user's spent amount
    user_discount = 0
    if current_user:
        user = User.query.get(current_user.id)

    user_discount = user.get_user_discount_amount() * float(new_bid)
    print(f"User discount: {user_discount}")
    final_amount = int(new_bid) - user_discount

    return render_template(
        "bidding_payment.html",
        car_id=car_id,
        new_bid=new_bid,
        user_id=user_id,
        user_discount=user_discount,
        final_amount=final_amount,
    )


@seller.route("/make-payment", methods=["GET", "POST"])
def make_payment():
    """
    Handles the make payment route.

    This function handles both GET and POST requests. If the request method is POST, it retrieves the form data. 
    If a car ID is provided and no payment is made yet, it retrieves the car from the database and renders the 'make_payment.html' template with the car. 
    If a car ID is provided and a payment is made, it retrieves the card details from the form data, validates the card details, 
    and if valid, processes the payment, updates the user's balance and spent amount, updates the car's status, and redirects to the 'my_invoices' route. 
    If the card details are not valid, it prints an error message. Regardless of the request method, it then renders the 'make_payment.html' template.

    Args:
        None

    Returns:
        str: The rendered 'make_payment.html' template with the car if a car ID is provided and no payment is made yet, 
        or without any arguments if a payment is made or the request method is GET.
    """
    if request.method == "POST":
        print(request.form)
        car_id = request.form.get("car_id", None)
        is_payment = request.form.get("payment", None)
        if car_id is not None and is_payment is None:
            print("-x-" * 20)
            print(f"Forwarded from car_id: {car_id} to make payment page...")
            print("-x-" * 20)

            car = Car.query.get(car_id)
            print(f"Car: {car}")
            return render_template("make_payment.html", car=car)

        if is_payment is not None and car_id is not None:
            print("-x-" * 20)
            print("Payment request received...")
            print("-x-" * 20)
            card_number = request.form.get("card_number", None)
            expiry = request.form.get("expiry", None)
            cvv = request.form.get("cvv", None)
            print(f"Card: {card_number}, Expiry: {expiry}, CVV: {cvv}")
            if card_number and expiry and cvv:
                print("Processing payment...")
                is_valid_card = Card.query.filter_by(card_number=card_number).first()
                if is_valid_card:
                    if all(
                        [is_valid_card.expiry_date == expiry, is_valid_card.cvv == cvv]
                    ):
                        car = Car.query.get(car_id)
                        print("Card Info Matched...")
                        print(f"Debiting {car.price} from {current_user}")

                        user = User.query.get(current_user.id)
                        balance = int(user.balance)
                        new_balance = balance - int(car.price)
                        user.balance = new_balance

                        spent_amount = int(user.spent_amount)
                        user.spent_amount = spent_amount + int(car.price)

                        db.session.commit()
                        print("Payment successful...")

                        car.status = "Booked"
                        db.session.commit()
                        print("Car status updated to Booked...")

                        return redirect(url_for("seller.my_invoices"))
                    else:
                        print("Card Info Mismatch")
                else:
                    print("Invalid payment details")

            else:
                print("Invalid payment details")

        return render_template("make_payment.html")
    return render_template("make_payment.html")


@seller.route("/listings")
def listings():
    cars = Car.query.all()
    template = "full"
    return render_template("listings.html", cars=cars, template=template)


@seller.route("/bid_done", methods=["GET", "POST"])
def bid_done():
    """
    Handles the bid done route.

    This function handles both GET and POST requests. If the request method is POST, it redirects to the 'bidding_payment' route. 
    Regardless of the request method, it retrieves the car ID, new bid, and user ID from the session, 
    and then renders the 'bid_done.html' template with these details.

    Args:
        None

    Returns:
        str: The rendered 'bid_done.html' template with the car ID, new bid, and user ID.
    """

    if request.method == "POST":
        return redirect(url_for("seller.bidding_payment"))

    car_id = session.get("car_id", None)
    new_bid = session.get("new_bid", None)
    user_id = session.get("user_id", None)

    return render_template(
        "bid_done.html", car_id=car_id, new_bid=new_bid, user_id=user_id
    )


@seller.route("/biddings", methods=["GET", "POST"])
def biddings():
    """
    Handles the biddings route.

    This function handles both GET and POST requests. 
    If the request method is POST, it retrieves the car ID and new bid from the form data.
    If a car ID and new bid are provided, it retrieves the car from the database, and if the new bid is greater than or equal to the car's bidding amount,
    it stores the car ID, new bid, and user ID in the session and redirects to the 'bid_done' route.
    If the new bid is less than the car's bidding amount, it updates the car's current bid and status, commits the changes to the database,
    and redirects to the 'biddings' route. Regardless of the request method, it retrieves all cars with a status of "Bidding" from the database,
    and then renders the 'biddings.html' template with these cars.

    Args:
        None

    Returns:
        str: The rendered 'biddings.html' template with all cars with a status of "Bidding".
    """
    if request.method == "POST":
        print(request.form)
        car_id = request.form.get("car_id", None)
        new_bid = request.form.get("bid_amount", None)

        if car_id and new_bid:
            car = Car.query.get(car_id)
            print(f"Car: {car}")
            print(f"New Bid amount: {new_bid}")
            print(f"Accepting bid: {car.bidding_amount}")

            if int(new_bid) >= int(car.bidding_amount):
                print(new_bid, car.bidding_amount)
                session["car_id"] = car_id
                session["new_bid"] = new_bid
                session["user_id"] = current_user.id
                return redirect(url_for("seller.bid_done"))

            car.current_bid = new_bid if new_bid != "1" else car.current_bid
            car.status = "Bidding"
            db.session.commit()
            print(f"Car {car_id} added to bidding with bid amount {new_bid}")
            return redirect(url_for("seller.biddings"))

    cars = Car.query.filter_by(status="Bidding").all()
    print(cars)
    return render_template("biddings.html", cars=cars)


@seller.route("/my-invoices")
@login_required
def my_invoices():
    return render_template("my_invoices.html")


@seller.route("/invoice")
@login_required
def invoice():
    return render_template("invoice.html")


@seller.route("/my-cars", methods=["GET", "POST"])
@login_required
def my_cars():
    print(
        "Fetching cars..."
        f"User: {current_user}-{current_user.id} \
            {current_user.get_all_cars()} {current_user.get_cars_count()}"
    )
    cars = Car.query.filter_by(user_id=current_user.id).all()
    return render_template("my_cars.html", cars=cars)


@seller.route("/create-listing", methods=["GET", "POST"])
def create_listing():
    if request.method == "POST":
        print(request.form)
        title = request.form.get("title", None)
        make = request.form.get("make", None)
        model = request.form.get("model", None)
        year = request.form.get("year", None)
        price = request.form.get("price", None)
        mileage = request.form.get("mileage", None)
        color = request.form.get("color", None)
        transmission = request.form.get("transmission", None)
        fuel_type = request.form.get("fuel", None)
        engine = request.form.get("engine", None)
        description = request.form.get("details", None)
        try:
            print("Creating a new car...")
            new_car = Car(
                title=title,
                make=make,
                model=model,
                year=year,
                price=price,
                mileage=mileage,
                color=color,
                transmission=transmission,
                fuel_type=fuel_type,
                engine=engine,
                description=description,
            )
            new_car.user_id = current_user.id
            db.session.add(new_car)
            db.session.commit()
            print(f"Car created: {new_car} by {current_user}")
        except Exception as e:
            print(e)

        return redirect(url_for("views.index"))

    return render_template("create_listing.html")


@seller.route("edit-car/<int:id>", methods=["GET", "POST"])
def edit_listing(id):
    car = Car.query.get(id)
    if request.method == "POST":
        print(request.form)
        car.title = request.form.get("title", None)
        car.make = request.form.get("make", None)
        car.model = request.form.get("model", None)
        car.year = request.form.get("year", None)
        car.price = request.form.get("price", None)
        car.mileage = request.form.get("mileage", None)
        car.color = request.form.get("color", None)
        car.transmission = request.form.get("transmission", None)
        car.fuel_type = request.form.get("fuel", None)
        car.engine = request.form.get("engine", None)
        car.description = request.form.get("details", None)
        car.status = request.form.get("status", None)
        car.bidding_amount = request.form.get("bidding_amount", None)

        # Current bid is 20% of the bidding amount
        car.current_bid = str(int(car.bidding_amount) * 0.2)

        try:
            print("Editing car...")
            db.session.commit()
            print(f"Car edited: {car} by {current_user}")
        except Exception as e:
            print(e)

        return redirect(url_for("views.index"))

    return render_template("edit_car.html", car=car)


@seller.route("/component-import-requests", methods=["GET", "POST"])
def all_component_import_requests():
    # Get all component import requests
    my_components = CarComponent.query.all()
    print(my_components)

    return render_template(
        "component_import_requests.html", my_components=my_components
    )


@seller.route("/update-component-status/<int:id>", methods=["POST"])
def update_component_status(id):
    print(f"Component ID: {id} updating status...")
    print(f"Request args: {request.form}")
    component = CarComponent.query.get(id)
    if component:
        # Assuming the name of the select element is 'select'
        new_status = request.form.get("select")
        component.status = new_status
        db.session.commit()
        return f"Component status updated to {new_status}!"
    else:
        return "Component not found", 404


@seller.route("/test", methods=["GET", "POST"])
def test():
    return render_template("signup.html")


@seller.route("/add-car-to-bid", methods=["POST", "GET"])
def add_car_to_bid():
    if request.method == "POST":
        print(request.form)
        car_id = request.form.get("car_id", None)
        if car_id:
            car = Car.query.get(car_id)
            if car.get_owner_id() != current_user.id:
                return "You are not authorized to add this car to bid", 403

            print(f"Adding car to bid: {car}")
            car.status = "Bidding"
            db.session.commit()
            return redirect(url_for("seller.my_cars"))
    return render_template("add_car_to_bid.html")
