from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static",
        template_folder="templates",
    )

    app.config["SECRET_KEY"] = "SUPERSECRETKEY"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/carmgmt"

    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth
    from .admin import admin
    from .buyer import buyer
    from .seller import seller

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(buyer, url_prefix="/")
    app.register_blueprint(seller, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        The function `load_user` retrieves a user from the database based on the provided ID.
        
        :param id: The `load_user` function takes an `id` parameter, which is used to retrieve a user
        from the database using SQLAlchemy's `User.query.get()` method. The `id` parameter should be an
        integer representing the unique identifier of the user you want to load
        :return: The function `load_user(id)` is returning a user object from the database based on the
        provided `id`. It uses the `User.query.get(int(id))` method to retrieve the user with the
        corresponding `id`.
        """
        return User.query.get(int(id))

    return app
