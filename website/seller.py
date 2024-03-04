from flask import Blueprint
from flask import render_template, request
from flask import redirect
from flask_login import login_required, current_user
from flask import url_for
from .models import Car, User, Card
from . import db
from .views import views

seller = Blueprint('seller', __name__, template_folder='templates/seller')


@seller.route('/make-payment', methods=['GET', 'POST'])
def make_payment():
    if request.method == 'POST':

        car_id = request.form.get('car_id', None)
        is_payment = request.form.get('payment', None)
        if car_id is not None and is_payment is None:
            print("-x-" * 20)
            print(f"Forwarded from car_id: {car_id} to make payment page...")
            print("-x-" * 20)


            car = Car.query.get(car_id)
            print(f"Car: {car}")
            return render_template('make_payment.html', car=car)

        if is_payment is not None:
            print("-x-" * 20)
            print(f"Payment request received...")
            print("-x-" * 20)


            # ImmutableMultiDict([('payment', 'True'), ('card_number', '1234'), ('expiry', '1234'), ('cvv', '1234')])
            # Get Card, Expiry and CVV then check and process payment
            card_number = request.form.get('card_number', None)
            expiry = request.form.get('expiry', None)
            cvv = request.form.get('cvv', None)
            print(f"Card: {card_number}, Expiry: {expiry}, CVV: {cvv}")
            if card_number and expiry and cvv:
                print(f"Processing payment...")
                is_valid_card = Card.query.filter_by(
                    card_number=card_number).first()
                if is_valid_card:
                    if all([is_valid_card.expiry == expiry, is_valid_card.cvv == cvv]):
                        print(f"Card Info Matched...")
                        print(f"Debiting {car.price} from {current_user}")
                        
                        user = User.query.get(current_user.id)
                        user.balance -= car.price
                        db.session.commit()
                        print(f"Payment successful...")
                        
                        car = Car.query.get(car_id)
                        car.status = "Booked"
                        db.session.commit()
                        print(f"Car status updated to Booked...")
                        
                        return redirect(url_for('seller.my_invoices'))
                    else:
                        print(f"Card Info Mismatch")
                else:
                    print(f"Invalid payment details")

            else:
                print(f"Invalid payment details")

        return render_template('make_payment.html')
    return render_template('make_payment.html')


@seller.route('/listings')
def listings():
    cars = Car.query.all()
    template = 'full'
    return render_template('listings.html', cars=cars, template=template)


@seller.route('/my-invoices')
@login_required
def my_invoices():
    return render_template('my_invoices.html')


@seller.route('/invoice')
@login_required
def invoice():
    return render_template('invoice.html')


@seller.route('/my-cars', methods=['GET', 'POST'])
@login_required
def my_cars():
    cars = Car.query.filter_by(user_id=current_user.id).all()
    return render_template('my_cars.html', cars=cars)


@seller.route('/create-listing', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        print(request.form)
        title = request.form.get('title', None)
        make = request.form.get('make', None)
        model = request.form.get('model', None)
        year = request.form.get('year', None)
        price = request.form.get('price', None)
        mileage = request.form.get('mileage', None)
        color = request.form.get('color', None)
        transmission = request.form.get('transmission', None)
        fuel_type = request.form.get('fuel', None)
        engine = request.form.get('engine', None)
        description = request.form.get('details', None)
        try:
            print(f"Creating a new car...")
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
                description=description
            )
            new_car.user_id = current_user.id
            db.session.add(new_car)
            db.session.commit()
            print(f"Car created: {new_car} by {current_user}")
        except Exception as e:
            print(e)

        return redirect(url_for('views.index'))

    return render_template('create_listing.html')


@seller.route('edit-car/<int:id>', methods=['GET', 'POST'])
def edit_listing(id):
    car = Car.query.get(id)
    if request.method == 'POST':
        print(request.form)
        car.title = request.form.get('title', None)
        car.make = request.form.get('make', None)
        car.model = request.form.get('model', None)
        car.year = request.form.get('year', None)
        car.price = request.form.get('price', None)
        car.mileage = request.form.get('mileage', None)
        car.color = request.form.get('color', None)
        car.transmission = request.form.get('transmission', None)
        car.fuel_type = request.form.get('fuel', None)
        car.engine = request.form.get('engine', None)
        car.description = request.form.get('details', None)
        try:
            print(f"Editing car...")
            db.session.commit()
            print(f"Car edited: {car} by {current_user}")
        except Exception as e:
            print(e)

        return redirect(url_for('views.index'))

    return render_template('edit_car.html', car=car)
