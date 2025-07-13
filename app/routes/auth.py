from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.utils.auth import verify_basic_auth
from app.utils.validators import Validators
from app.models.user import Users
from flask import Response
from app.controllers.user_controller import UserController


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    required_fields = ['username', 'password', 'email', 'phone_number']
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"message": f"Missing fields: {', '.join(missing_fields)}"}), 400

    response, error = UserController().create_user(data)
    if error:
        return jsonify(response), 400

    return jsonify(response), 201

@bp.route('/login', methods=['POST'])
def login():
    response, is_verified = verify_basic_auth()
    if is_verified:
        return jsonify({"message": "Login successful"}), 200
    else :
        return jsonify({"message": "Invalid credentials"}), 400

@bp.route('/update', methods=['PUT'])
def update_user():
    response, is_verified = verify_basic_auth()
    if not is_verified:
        return response, 401 # Unauthorized
    
    user = response  # The user object is returned from verify_basic_auth
    
    data = request.get_json() or {}

    if not data.get('username'):
        return jsonify({"message": "Username is required"}), 400

    response, error = UserController().update_user(user.id, data)
    if error:
        return jsonify(response), 400

    return jsonify(response), 200
#@bp.route('/test', methods=['GET'])
#def test():