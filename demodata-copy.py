from website import create_app, db
from website.models import User, Car, CarRequest


def create_demo_data():
    app = create_app()
    with app.app_context():
        # Create users
        users_data = [
            {
                "email": f"user{i}@user.com",
                "first_name": f"User{i}",
                "last_name": "Demo",
                "type": f"Type{i}",
            }
            for i in range(1, 10)
        ]
        for user_data in users_data:
            user = User(**user_data)
            user.set_password("1234")
            db.session.add(user)

        # Create cars
        cars_data = [
            {
                "title": f"Car{i}",
                "make": "Toyota",
                "model": "Corolla",
                "year": "2022",
                "price": "20000",
                "mileage": "5000",
                "color": "Black",
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "engine": "2.0L",
                "description": "Demo car",
            }
            for i in range(1, 10)
        ]
        for car_data in cars_data:
            car = Car(
                **car_data, user_id=1
            )  # Assuming all cars belong to user with ID 1
            db.session.add(car)

        # Create car requests
        car_requests_data = [
            {
                "title": f"Request{i}",
                "make": "BMW",
                "model": "X5",
                "year": "2023",
                "color": "White",
                "details": "Demo request",
            }
            for i in range(1, 10)
        ]
        for request_data in car_requests_data:
            car_request = CarRequest(
                **request_data, user_id=2
            )  # Assuming all requests made by user with ID 2
            db.session.add(car_request)

        # Commit changes to the database
        db.session.commit()


def print_demo_data():
    app = create_app()
    with app.app_context():
        print("Users:")
        for user in User.query.all():
            print(f"ID: {user.id}, Email: {user.email}, Type: {user.type}")

        print("\nCars:")
        for car in Car.query.all():
            print(
                f"ID: {car.id}, Title: {car.title}, Make: {car.make}, Model: {car.model}"
            )

        print("\nCar Requests:")
        for request in CarRequest.query.all():
            print(
                f"ID: {request.id}, Title: {request.title}, Make: {request.make}, Model: {request.model}"
            )


if __name__ == "__main__":
    create_demo_data()
    print_demo_data()
