from flask import Blueprint, request, jsonify
from flask import request
from app.controllers.car_controller import CarController
from app.utils.auth import verify_basic_auth

bp = Blueprint('car', __name__, url_prefix='/car')


@bp.route('/add', methods=['POST'])
def add_car():
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized

    user = response  # The user object is returned from verify_basic_auth

    if user.type != 'merchant':
       return jsonify({"message": "Only merchants can add cars."}), 403

    data = request.get_json()

    data['merchant_id'] = user.id  # Set the merchant_id from the authenticated user

    required_fields = ['make', 'model', 'year', 'price_per_day']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields."}), 400
    
    response, error = CarController().add_car(data)

    if error:
        return jsonify(response), 400

    return response

@bp.route('/update/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized

    user = response  # The user object is returned from verify_basic_auth

    if user.type != 'merchant':
       return jsonify({"message": "Only merchants can update their own cars."}), 403
    
    data = request.get_json()
    required_fields = ['make', 'model', 'year', 'price_per_day']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields."}), 400

    response, error = CarController().update_car(user.id, car_id, data)
    
    if error:
        return jsonify(response), 400
    return response

@bp.route('/delete/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized

    user = response  # The user object is returned from verify_basic_auth

    if user.type != 'merchant':
       return jsonify({"message": "Only merchants can delete their own cars."}), 403
    
    response, error = CarController().delete_car(user.id, car_id)

    if error:
        return jsonify(response), 400

    return jsonify({"message": "Car deleted successfully."}), 200

@bp.route('/list', methods=['GET'])
def get_cars():
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized

    filter_keys = ['make', 'model', 'year', 'price_min', 'price_max', 'merchant_id']
    filters = {key: request.args.get(key) for key in filter_keys if key in request.args}

    response, error = CarController().get_cars(filters)

    if error:
        return jsonify(response), 404

    return jsonify(response), 200