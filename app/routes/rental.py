from flask import Blueprint, jsonify, request
from app.controllers.user_controller import UserController
from app.controllers.rental_controller import RentalController
from app.utils.auth import verify_basic_auth

bp = Blueprint('rental', __name__, url_prefix='/rental')

@bp.route('/rent/<int:car_id>', methods=['POST'])
def rent_car(car_id):
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized

    user = response  # The user object is returned from verify_basic_auth

    response, error = RentalController().rent_car(car_id, user.id)

    if error:
        return jsonify(response), 400
    
    return jsonify(response), 200

@bp.route('/return/<int:car_id>', methods=['POST'])
def return_car(car_id):
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized

    user = response  # The user object is returned from verify_basic_auth

    response, error = RentalController().return_car(car_id, user.id)

    if error:
        return jsonify(response), 400
    
    return jsonify(response), 200

@bp.route('/history/<string:username>', methods=['GET'])
def rental_history(username):
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized

    session_user = response  # The user object is returned from verify_basic_auth

    user = UserController().get_user_by_username(username)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if user.id != session_user.id and session_user.type != 'admin':
        return jsonify({"message": "You are not authorized to view this user's rental history"}), 403
    
    # Get optional filters from query parameters for rentals
    filter_keys = ['rented_before', 'rented_after', 'returned_after', 'returned_before', 'car_id']
    filters = {key: request.args.get(key) for key in filter_keys if request.args.get(key) is not None}
    filters["user_id"] = user.id
    #filters["rented_at"] = "2025-07-13"

    response, error = RentalController().get_rentals(filters)

    if error:
        return jsonify(response), 400
    
    return jsonify(response), 200
