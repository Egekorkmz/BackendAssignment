from enum import Enum
from app import db

class CarState(Enum):
    AVAILABLE = 1
    RENTED = 2
    DELETED = 3

class Cars(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    year = db.Column(db.Integer)
    price_per_day = db.Column(db.Float)
    state = db.Column(db.Enum(CarState), nullable=False, default=CarState.AVAILABLE)

    rentals = db.relationship('Rental', backref='cars', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "price_per_day": self.price_per_day,
            "merchant_id": self.merchant_id,
            "state": self.state
        }