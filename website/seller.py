from flask import Blueprint
from flask import render_template, request
from flask import redirect
from flask_login import login_required, current_user
from flask import url_for
from .models import Car
from . import db
from .views import views

seller = Blueprint('seller', __name__, template_folder='templates/seller')


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
