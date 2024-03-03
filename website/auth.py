from flask import Blueprint
from flask import render_template, request
from flask import redirect
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(email, password)

        user = User.query.filter_by(email=email).first()

        if user:
            if user.check_password(password):
                print('User logged in')
                return redirect(url_for('views.home'))
            else:
                print('Password incorrect')
        else:
            print('User does not exist')

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        # ([('first_name', 'Zulkar'), ('last_name', 'Nain'), ('email', 'zulkarnain@gmail.com'), ('password', '1234'), ('password_confirmation', '1234'), ('user_type', 'admin'), ('marketing_accept', 'on')])
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        user_type = request.form.get('user_type')
        marketing_accept = request.form.get('marketing_accept')

        if password != password_confirmation:
            print('Password does not match')
        else:
            # Create a new user and add it to the database

            # Check if the user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print('User already exists')
            else:
                new_user = User(email=email, first_name=first_name,
                                last_name=last_name, type=user_type)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                print('User created', new_user)
                return redirect(url_for('auth.login'))

    return render_template('signup.html')
