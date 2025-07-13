from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import routes and models to register them
    from app.routes import auth, car, rental
    from app import models

    app.register_blueprint(car.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(rental.bp)

    return app
