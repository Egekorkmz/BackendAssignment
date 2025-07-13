from app import db
from app.models.car import CarState, Cars
from datetime import datetime
from app.models.rental import Rental
from app.utils.validators import Validators

class RentalController:
    @staticmethod
    def rent_car(car_id, user_id):
        rented_car = db.session.query(Rental).filter_by(user_id=user_id, returned_at=None).first()
        if rented_car:
            # User already has this car rented and not returned yet
            return {"message": "You have already rented car and it is not returned yet."}, True

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
            query = db.session.query(Rental)
            
            filter_args = {}
            time_filters = {}

            for key, value in filter_by.items():
                if key in ["rented_before", "rented_after", "returned_before", "returned_after"]:
                    try:
                        if Validators.is_valid_iso_date(value):
                            time_filters[key] = datetime.fromisoformat(value)
                    except ValueError:
                        return {"message": f"Invalid datetime format for {key}. Use ISO 8601 format."}, True
                else:
                    filter_args[key] = value  # for exact match filters

            query = Rental.query

            # Apply exact match filters if needed
            if filter_args:
                query = query.filter_by(**filter_args)

            # Apply time-based filters cleanly
            if "rented_before" in time_filters:
                query = query.filter(Rental.rented_at < time_filters["rented_before"])
            if "rented_after" in time_filters:
                query = query.filter(Rental.rented_at > time_filters["rented_after"])
            if "returned_before" in time_filters:
                query = query.filter(Rental.returned_at.isnot(None), Rental.returned_at < time_filters["returned_before"])
            if "returned_after" in time_filters:
                query = query.filter(Rental.returned_at.isnot(None), Rental.returned_at > time_filters["returned_after"])

            rentals = query.all()
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
