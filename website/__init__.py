from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__,
                static_url_path='/',
                static_folder='static',
                template_folder='templates',
                )

    app.config['SECRET_KEY'] = 'SUPERSECRETKEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root@localhost/carmgmt"

    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth
    from .admin import admin
    from .buyer import buyer
    from .seller import seller
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(buyer, url_prefix='/')
    app.register_blueprint(seller, url_prefix='/')

    from .models import User, Car
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
