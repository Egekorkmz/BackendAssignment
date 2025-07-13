from flask import Blueprint, jsonify
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
    
    if user.id != session_user['id'] and session_user['type'] != 'admin':
        return jsonify({"message": "You are not authorized to view this user's rental history"}), 403
    
    #TODO: please add a filter
    response, error = RentalController().get_rentals({"user_id": user.id})

    if error:
        return jsonify(response), 400
    
    return jsonify(response), 200
