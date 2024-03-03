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
    
    ## User Type:
    # 1. Admin
    # 2. Buyer
    # 3. Seller
    
    type = db.Column(db.String(150), nullable=True)
    cars = db.relationship('Car')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(150), nullable=True)
    model = db.Column(db.String(150), nullable=True)
    year = db.Column(db.String(150), nullable=True)
    price = db.Column(db.String(150), nullable=True)
    mileage = db.Column(db.String(150), nullable=True)
    color = db.Column(db.String(150), nullable=True)
    transmission = db.Column(db.String(150), nullable=True)
    fuel_type = db.Column(db.String(150), nullable=True)
    engine = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
