from app import db
from app.models.car import Cars
from app.controllers.user_controller import UserController
from app.models.car import CarState

class CarController:
    # Get all cars for a specific merchant by merchant_id
    def get_cars_by_merchantID(self, merchant_id):
        cars = db.session.query(Cars).filter_by(merchant_id=merchant_id).filter(Cars.state != CarState.DELETED).all()
        
        if not cars:
            return {"message": "No cars found for this merchant"}, True
        
        # Convert the list of Cars objects to a list of dictionaries
        car_list = []
        for car in cars:
            car_list.append(car.to_dict)

        return car_list, False
            
    # Get a single car by its ID
    def get_car_by_id(self, car_id):
        car = db.session.query(Cars).filter_by(id=car_id).first()
        
        if not car:
            return {"message": "Car not found"}, True
        
        return car, False
    
    # Get all cars, optionally filtered by provided criteria
    def get_cars(self, filter_by=None):
        if filter_by:
            cars = db.session.query(Cars).filter_by(**filter_by).filter(Cars.state != CarState.DELETED).all()
        else:
            cars = db.session.query(Cars).filter(Cars.state != CarState.DELETED).all()
        
        if not cars:
            return {"message": "No cars found"}, True
        
        # Get all merchants for car-merchant mapping
        merchants, error = UserController().get_merchants()
        if not merchants:
            return {"message": "No merchants found"}, True
        
        # Build car list with merchant info
        car_list = []
        for car in cars:
            merchant = next((m for m in merchants["merchants"] if m["id"] == car.merchant_id), None)

            car_dict = {
                "id": car.id,
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "price_per_day": car.price_per_day,
                "state": car.state.name,  # Convert enum to string
                "merchant": merchant
            }
            car_list.append(car_dict)
        
        return car_list, False

    # Add a new car to the database
    def add_car(self, data):
        required_fields = ['make', 'model', 'year', 'price_per_day']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return {"message": f"Missing fields: {', '.join(missing_fields)}"}, True
        
        # Validate that year and price_per_day are numeric
        if not str(data['year']).isdigit():
            return {"message": "Invalid year format"}, True
        try:
            float(data['price_per_day'])
        except (ValueError, TypeError):
            return {"message": "Invalid price format"}, True
        
        car = Cars(
            merchant_id=data['merchant_id'],
            make=data['make'],
            model=data['model'],
            year=data['year'],
            price_per_day=data['price_per_day'],
            state=CarState.AVAILABLE  # Use the enum value
        )
        
        db.session.add(car)
        db.session.commit()
        
        car_dict = {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "price_per_day": car.price_per_day,
            "state": car.state.name,  # Convert enum to string
            "merchant_id": car.merchant_id
        }

        return {"message": "Car added successfully", "car": car_dict}, False
    
    # Update an existing car's details
    def update_car(self, merchant_id, car_id, data):
        car = db.session.query(Cars).filter_by(id=car_id).filter(Cars.state != CarState.DELETED).first()
        
        if not car:
            return {"message": "Car not found"}, True
        
        if car.merchant_id != merchant_id:
            return {"message": "Unauthorized to update this car"}, True
        
        # Update only provided fields
        for field in ['make', 'model', 'year', 'price_per_day', 'available']:
            if field in data:
                setattr(car, field, data[field])
        
        db.session.commit()
        return {"message": "Car updated successfully"}, False
    
    # Soft-delete a car (mark as DELETED, don't remove from DB)
    def delete_car(self, merchant_id, car_id):
        car = db.session.query(Cars).filter_by(id=car_id).first()
        
        if not car:
            return {"message": "Car not found"}, True
        
        if car.merchant_id != merchant_id:
            return {"message": "Unauthorized to delete this car"}, True
        
        car.state = CarState.DELETED  # Set the state to DELETED instead of removing it from the database because rent history should be preserved
        db.session.commit()
        
        return {"message": "Car deleted successfully"}, False