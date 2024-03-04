from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import datetime


class User(db.Model, UserMixin):

    def __init__(self, *args, **kwargs):
        print("Saving user...")
        super(User, self).__init__(*args, **kwargs)
        print("User saved!")
        db.session.add(self)
        db.session.commit()
        
        print("Creating card...")
        self.create_card()
        print("Card created!")
        print("User created!")
        

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    balance = db.Column(db.Integer, default=0)
    subscription = db.Column(db.String(150), nullable=True)

    # User Type:
    # 1. Admin
    # 2. Buyer
    # 3. Seller

    type = db.Column(db.String(150), nullable=True)
    cars = db.relationship('Car')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_all_cars(self):
        return Car.query.filter_by(user_id=self.id).all()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_cars_count(self):
        return len(Car.query.filter_by(user_id=self.id).all())

    def create_card(self):
        while True:
            id = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))
            card = Card.query.filter_by(id=id).first()
            if not card:
                break

        while True:
            first_digit = str(random.choice(range(1, 10)))  
            other_digits = ''.join(random.choices(string.digits, k=15)) 
            card_number = first_digit + other_digits
            if not card:
                break

        card_holder = self.get_full_name()
        expiry_date = (datetime.date.today() + datetime.timedelta(
            days=random.randint(365, (365*random.randint(1, 10))))).strftime('%m/%y')
        cvv = ''.join(random.choices(string.digits, k=3))
        new_card = Card(
            id=id,
            card_number=card_number,
            card_holder=card_holder,
            expiry_date=expiry_date,
            cvv=cvv
        )

        print(f"Creating card for {self.get_full_name()}...")
        print(f"Adding card to {self.id}...")
        new_card.user_id = self.id
        db.session.add(new_card)
        db.session.commit()
        return new_card

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} <{self.email}>'


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=True)
    # make types
    # 1. Toyota
    # 2. Honda
    # 3. BMW

    make = db.Column(db.String(150), nullable=True)
    model = db.Column(db.String(150), nullable=True)
    year = db.Column(db.String(150), nullable=True)
    price = db.Column(db.String(150), nullable=True)
    mileage = db.Column(db.String(150), nullable=True)
    color = db.Column(db.String(150), nullable=True)
    # transmission types
    # 1. Automatic
    # 2. Manual
    transmission = db.Column(db.String(150), nullable=True)
    # fuel type
    # 1. Petrol
    # 2. Diesel
    # 3. Electric
    # 4. Hybrid
    # 5. LPG
    fuel_type = db.Column(db.String(150), nullable=True)

    # engine types
    # 1. 1.0L
    # 2. 1.5L
    # 3. 2.0L

    engine = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def get_owner_name(self):
        return User.query.filter_by(id=self.user_id).first()


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(150), nullable=True)
    card_holder = db.Column(db.String(150), nullable=True)
    expiry_date = db.Column(db.String(150), nullable=True)
    cvv = db.Column(db.String(150), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def get_card_balance(self):
        return User.query.filter_by(id=self.user_id).first().balance

    def __str__(self) -> str:
        return f'{self.card_holder} <{self.card_number}>'
