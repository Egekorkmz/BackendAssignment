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
    if verify_basic_auth():
        return jsonify({"message": "Login successful"}), 200
    else :
        return jsonify({"message": "Invalid credentials"}), 400

#@bp.route('/test', methods=['GET'])
#def test():