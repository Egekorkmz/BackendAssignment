from flask import request, session, jsonify
from werkzeug.security import check_password_hash
from app.models.user import Users
    
def verify_basic_auth():
    data = request.authorization

    if not data or not data.username or not data.password:
        return jsonify({"message": "Missing Basic Auth headers"}), False

    user = Users.query.filter_by(username=data.username).first()
    if user and check_password_hash(user.password_hash, data.password):
        return user, True
    else:
        return jsonify({"message": "Missing Basic Auth headers"}), False