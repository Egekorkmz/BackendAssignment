from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from app import db
from app.utils.validators import Validators
from app.models.user import Users
from flask import Response

class UserController:

    def get_user_by_id(self, user_id):
        user = db.session.query(Users).filter_by(id=user_id).first()
        
        if not user:
            return {"message": "User not found"}, True
        
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "type": user.type
        }
        
        return user_dict, False

    def get_user_by_username(self, username):
        user = db.session.query(Users).filter_by(username=username).first()
        
        return user
    
    def get_merchants(self):
        merchants = db.session.query(Users).filter_by(type='merchant').all()
        
        if not merchants:
            return {"message": "No merchants found"}, True
        
        merchant_list = []
        for merchant in merchants:
            merchant_list.append({
                "id": merchant.id,
                "username": merchant.username,
                "email": merchant.email,
                "phone_number": merchant.phone_number
            })
        
        return {"merchants": merchant_list}, False
    
    def create_user(self, data):
        required_fields = ['username', 'password', 'email', 'phone_number', 'type']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return {"message": f"Missing fields: {', '.join(missing_fields)}"}, True
        
        if not Validators.is_valid_email(data['email']):
            return {"message": "Invalid email format"}, True
        
        if not Validators.is_valid_phone(data['phone_number']):
            return {"message": "Invalid phone number format"}, True
        
        if Users.query.filter_by(username=data['username']).first():
            return {"message": "Username already exists"}, True
        
        type = data.get('type', 'user')
        if type not in ['user', 'merchant']:
            return jsonify({"message": "Role must be 'user' or 'merchant'"}), True
        
        user = Users(
            username=data['username'],
            password_hash=generate_password_hash(data['password']),
            email=data['email'],
            phone_number=data['phone_number'],
            type=data['type']
        )
        
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully", "user_id": user.id}, False
    
    def update_user(self, user_id, data):
        user = db.session.query(Users).filter_by(id=user_id).first()
        
        if not user:
            return {"message": "User not found"}, True
        
        for field in ['email', 'phone_number']:
            if field in data:
                setattr(user, field, data[field])
        
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        return {"message": "User updated successfully"}, False
    
    def delete_user(self, user_id):
        user = db.session.query(Users).filter_by(id=user_id).first()
        
        if not user:
            return {"message": "User not found"}, True
        
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, False

    