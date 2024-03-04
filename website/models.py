from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

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
