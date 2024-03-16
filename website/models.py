import datetime
import random
import string

from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(db.Model, UserMixin):
    def __init__(self, *args, **kwargs):
        """
        Initializes a new User instance and saves it to the database.

        This function is automatically called when a new User instance is created. 
        It calls the parent class's __init__ method to initialize the User instance, 
        saves the instance to the database, and then creates a new card for the user.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """

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
    active_status = db.Column(db.String(150), default="Active")
    spent_amount = db.Column(db.Integer, default=0)

    # User Type:
    # 1. Admin
    # 2. Buyer
    # 3. Seller

    type = db.Column(db.String(150), nullable=True)
    cars = db.relationship("Car")

    def set_password(self, password):
        """
        Sets the password for a user.

        This function takes a plain text password, hashes it using the generate_password_hash function from Werkzeug, 
        and then sets the hashed password as the user's password.

        Args:
            password (str): The plain text password that needs to be hashed and set for the user.

        Returns:
            None
        """

        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if a provided password matches the user's password.

        This function takes a plain text password, hashes it using the same method as the stored password, 
        and then compares the hashed password with the stored password hash.

        Args:
            password (str): The plain text password that needs to be checked.

        Returns:
            bool: True if the hashed password matches the stored password hash, False otherwise.
        """

        return check_password_hash(self.password, password)
    def get_all_cars(self):
        return Car.query.filter_by(user_id=self.id).all()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_cars_count(self):
        """
        Retrieves the count of cars associated with a user.

        This function queries the database to find all cars associated with the user's ID and returns the count of such cars.

        Args:
            None

        Returns:
            int: The count of cars associated with the user ID.
        """

        return len(Car.query.filter_by(user_id=self.id).all())

    def get_card_number(self):
        """
        Retrieves a card number associated with a user and formats it by adding spaces every four characters.

        This function queries the database to find the first card associated with the user's ID. 
        It then retrieves the card number, 
        splits it into groups of 4 digits, and joins these groups with spaces. 
        The formatted card number is then returned.

        Args:
            None

        Returns:
            str: The card number associated with the user ID in a formatted manner. The card number is split into groups of 4 digits and joined with spaces.
        """

        number = Card.query.filter_by(user_id=self.id).first().card_number
        return " ".join([number[i : i + 4] for i in range(0, len(number), 4)])

    def get_card_expiry_date(self):
        return Card.query.filter_by(user_id=self.id).first().expiry_date

    def get_card_cvv(self):
        return Card.query.filter_by(user_id=self.id).first().cvv

    def get_card_holder(self):
        return Card.query.filter_by(user_id=self.id).first().card_holder

    def get_card_balance(self):
        return Card.query.filter_by(user_id=self.id).first().balance

    def get_user_discount_amount(self):
        """
        Calculates the discount amount for a user based on their spent amount.

        This function calculates the discount amount by dividing the user's spent amount by a predefined discount per amount (30,000), 
        and then multiplying the result by a predefined discount rate per amount (0.01). The final discount amount is then returned.

        Args:
            None

        Returns:
            float: The discount amount for the user based on their spent amount.
        """

        discount_per_amount = 30_000
        discount_rate_per_amount = 0.01
        final_discount = (
            self.spent_amount // discount_per_amount * discount_rate_per_amount
        )
        return final_discount

    def create_card(self):
        """
        Creates a new card for the user.

        This function generates a unique 10-character ID and a unique 16-digit card number. It sets the card holder's name to the user's full name, 
        generates a random expiry date between 1 and 10 years from today, and a random 3-digit CVV. It then creates a new card with these details, 
        associates the card with the user, and adds the card to the database.

        Args:
            None

        Returns:
            Card: The newly created card.
        """

        # Generate a unique 10-character ID
        while True:
            id = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            card = Card.query.filter_by(id=id).first()
            if not card:
                break

        # Generate a unique 16-digit card number
        while True:
            first_digit = str(random.choice(range(1, 10)))
            other_digits = "".join(random.choices(string.digits, k=15))
            card_number = first_digit + other_digits
            if not card:
                break

        # Set the card holder's name to the user's full name
        card_holder = self.get_full_name()

        # Generate a random expiry date between 1 and 10 years from today
        expiry_date = (
            datetime.date.today()
            + datetime.timedelta(
                days=random.randint(365, (365 * random.randint(1, 10)))
            )
        ).strftime("%m/%y")

        # Generate a random 3-digit CVV
        cvv = "".join(random.choices(string.digits, k=3))

        # Create the new card
        new_card = Card(
            id=id,
            card_number=card_number,
            card_holder=card_holder,
            expiry_date=expiry_date,
            cvv=cvv,
        )

        # Print a message indicating that the card is being created
        print(f"Creating card for {self.get_full_name()}...")

        # Print a message indicating that the card is being added to the user
        print(f"Adding card to {self.id}...")

        # Associate the new card with the user
        new_card.user_id = self.id

        # Add the new card to the database
        db.session.add(new_card)

        # Commit the changes to the database
        db.session.commit()

        # Return the newly created card
        return new_card

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} <{self.email}>"


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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    status = db.Column(db.String(150), default="Available")
    bidding_amount = db.Column(db.String(150), nullable=True)
    current_bid = db.Column(db.String(150), nullable=True)

    def get_owner_name(self):
        return User.query.filter_by(id=self.user_id).first()

    def get_owner_id(self):
        return self.user_id


class CarRequest(db.Model):
    # ImmutableMultiDict([('title', 'BMW R10'), ('make', 'BMW'), ('model', 'RED'), ('year', '2020'), ('color', 'RED'), ('details', 'link-here')])
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=True)
    make = db.Column(db.String(150), nullable=True)
    model = db.Column(db.String(150), nullable=True)
    year = db.Column(db.String(150), nullable=True)
    color = db.Column(db.String(150), nullable=True)
    details = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(150), default="Pending")


class CarComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    component_name = db.Column(db.String(150), nullable=True)
    manufacturer = db.Column(db.String(150), nullable=True)
    details = db.Column(db.String(150), nullable=True)
    quantity = db.Column(db.String(150), nullable=True)

    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(150), default="Requested")

    def get_all_current_user_components(self):
        return CarComponent.query.filter_by(user_id=self.id).all()


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(150), nullable=True)
    card_holder = db.Column(db.String(150), nullable=True)
    expiry_date = db.Column(db.String(150), nullable=True)
    cvv = db.Column(db.String(150), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def get_card_balance(self):
        return User.query.filter_by(id=self.user_id).first().balance

    def get_card_number(self):
        return self.card_number

    def __str__(self) -> str:
        return f"{self.card_holder} <{self.card_number}>"
