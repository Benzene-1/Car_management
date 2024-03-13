from flask import Blueprint
from flask import render_template, request
from flask_login import current_user
from website import db
from website.models import CarRequest

buyer = Blueprint('buyer', __name__, template_folder='templates/buyer')


@buyer.route('/request-car', methods=['GET', 'POST'])
def request_car():
    if request.method == 'POST':
        print(request.form)
        title = request.form.get('title')
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        color = request.form.get('color')
        details = request.form.get('details')
        
        car_request = CarRequest(title=title, make=make, model=model, year=year, color=color, details=details, user_id=current_user.id)
        db.session.add(car_request)
        db.session.commit()
        
    return render_template('request_car_import.html')

@buyer.route('/request_car_parts', methods=['GET', 'POST'])
def request_car_parts():
    print(request.form)
    
    return render_template('request_car_parts.html')