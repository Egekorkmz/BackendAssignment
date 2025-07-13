from app import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = 'rental'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    rented_at = db.Column(db.DateTime, default=datetime.now)
    returned_at = db.Column(db.DateTime, nullable=True)
    total_price = db.Column(db.Float, nullable=True)