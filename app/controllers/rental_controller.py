from app import db
from app.models.car import CarState, Cars
from datetime import datetime
from app.models.rental import Rental

class RentalController:
    @staticmethod
    def rent_car(car_id, user_id):
        # Find the car by ID and ensure it is available
        car = db.session.query(Cars).filter_by(id=car_id, state=CarState.AVAILABLE).first()
        
        if not car:
            # Car not found or not available
            return {"message": "Car not found"}, True
        elif not car.state == CarState.AVAILABLE:
            # Car is not available for rental
            return {"message": "Car is not available for rental"}, True
        
        if car.merchant_id == user_id:
            # Prevent users from renting their own car
            return {"message": "Users cannot rent their own car."}, True
        
        # Create a new rental record
        rental = Rental(
            car_id=car.id,
            user_id=user_id,
        )
        db.session.add(rental)
        car.state = CarState.RENTED  # Update the car state to RENTED
        db.session.commit()
        
        # Return success message and rental ID
        return {"message": "Car rented successfully", "rental_id": rental.id}, False
    
    @staticmethod
    def return_car(car_id, user_id):
        # Find the rental record that matches car and user, and is not yet returned
        rental = db.session.query(Rental).filter_by(car_id=car_id, user_id=user_id, returned_at=None).first()
        if not rental:
            # Rental not found or already returned
            return {"message": "Rental not found or already returned"}, True

        rental.returned_at = datetime.now()  # Set return time
        days_rented = max((rental.returned_at - rental.rented_at).days, 1)  # Calculate days rented, minimum 1

        car = db.session.query(Cars).filter_by(id=car_id).first()
        if not car:
            # Car not found
            return {"message": "Car not found"}, True

        car.state = CarState.AVAILABLE  # Update the car state to AVAILABLE
        rental.total_price = days_rented * car.price_per_day  # Calculate total price

        db.session.commit()
        # Return success message, days rented, and total price
        return { 
            "message": f"Car {car.make} {car.model} returned successfully.",
            "days_rented": days_rented,
            "total_price": rental.total_price
        }, False
    
    @staticmethod
    def get_rentals(filter_by=None):
        # Optionally filter rentals by provided criteria
        if filter_by:
            rentals = db.session.query(Rental).filter_by(**filter_by).all()
        else:
            rentals = db.session.query(Rental).all()
        
        if not rentals:
            # No rentals found
            return {"message": "No rentals found"}, True
        
        rental_list = []
        for rental in rentals:
            # Get car details for each rental
            car = db.session.query(Cars).filter_by(id=rental.car_id).first()
            if car:
                rental_dict = {
                    "rental_id": rental.id,
                    "car_id": car.id,
                    "make": car.make,
                    "model": car.model,
                    "rented_at": rental.rented_at,
                    "returned_at": rental.returned_at,
                    "total_price": rental.total_price
                }
                rental_list.append(rental_dict)
        
        # Return list of rentals
        return rental_list, False
