import random
import string

from website import create_app, db
from website.models import Car, Card, CarRequest, User

app = create_app()


def generate_random_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_demo_data():
    # Create admin users
    for i in range(1, 6):
        email = f"admin{i}@admin.com"
        user = User(
            email=email,
            first_name=f"Admin {i}",
            last_name=f"User {i}",
            type="Admin",
        )
        user.set_password("1234")
        db.session.add(user)

    # Create buyer users
    for i in range(1, 11):
        email = f"buyer{i}@buyer.com"
        user = User(
            email=email,
            first_name=f"Buyer {i}",
            last_name=f"User {i}",
            type="Buyer",
        )
        user.set_password("1234")
        db.session.add(user)


    # Create seller users
    for i in range(1, 11):
        email = f"seller{i}@seller.com"
        user = User(
            email=email,
            first_name=f"Seller {i}",
            last_name=f"User {i}",
            type="Seller",
        )
        user.set_password("1234")
        db.session.add(user)

    # Create cars
    makes = ["Toyota", "Honda", "BMW"]
    models = ["Corolla", "Civic", "X5"]
    colors = ["Red", "Blue", "Black", "White", "Silver"]
    transmissions = ["Automatic", "Manual"]
    fuel_types = ["Petrol", "Diesel", "Electric", "Hybrid", "LPG"]
    engines = ["1.0L", "1.5L", "2.0L"]

    for user in User.query.filter_by(type="Seller").all():
        for i in range(random.randint(1, 5)):
            title = f"{random.choice(makes)} {random.choice(models)}"
            make = random.choice(makes)
            model = random.choice(models)
            year = str(random.randint(2000, 2023))
            price = str(random.randint(10000, 100000))
            mileage = str(random.randint(1000, 100000))
            color = random.choice(colors)
            transmission = random.choice(transmissions)
            fuel_type = random.choice(fuel_types)
            engine = random.choice(engines)
            description = generate_random_string(50)
            car = Car(
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
                user_id=user.id,
            )
            db.session.add(car)

    # Create car requests
    for user in User.query.filter_by(type="Buyer").all():
        for i in range(random.randint(1, 3)):
            title = generate_random_string(10)
            make = random.choice(makes)
            model = random.choice(models)
            year = str(random.randint(2000, 2023))
            color = random.choice(colors)
            details = generate_random_string(20)
            car_request = CarRequest(
                title=title,
                make=make,
                model=model,
                year=year,
                color=color,
                details=details,
                user_id=user.id,
            )
            db.session.add(car_request)

    db.session.commit()

    print("Demo data created successfully!")


def print_data_details():
    print("Users:")
    for user in User.query.all():
        print(f"- {user.get_full_name()} ({user.email}) - Type: {user.type}")
        cars = user.get_all_cars()
        if cars:
            print("  Cars:")
            for car in cars:
                print(
                    f"    - {car.title} ({car.make} {car.model}, {car.year}, {car.color})"
                )
        else:
            print("  No cars")

        card = Card.query.filter_by(user_id=user.id).first()
        if card:
            print(
                f"  Card: {card.get_card_number()} (Exp: {card.expiry_date}, CVV: {card.cvv}, Balance: {card.get_card_balance()})"
            )
        else:
            print("  No card")

    print("\nCar Requests:")
    for car_request in CarRequest.query.all():
        user = User.query.get(car_request.user_id)
        print(
            f"- {car_request.title} ({car_request.make} {car_request.model}, {car_request.year}, {car_request.color}) - Requested by: {user.get_full_name()} ({user.email})"
        )


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        generate_demo_data()
        print_data_details()
