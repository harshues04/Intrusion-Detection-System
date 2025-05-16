from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api

db = SQLAlchemy()
login_manager = LoginManager()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your generated key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    api.init_app(app)

    # Import models after app and db initialization
    with app.app_context():
        from app import models  # Import models module
        db.create_all()

    # Define user_loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import routes after models
    from app.routes import init_routes
    init_routes(app, api)

    return app