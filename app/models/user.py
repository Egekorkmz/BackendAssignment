from app import db

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), nullable=False)

    cars = db.relationship('Cars', backref='users', lazy=True)
    rentals = db.relationship('Rental', backref='users', lazy=True)

