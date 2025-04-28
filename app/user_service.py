from flask import Blueprint, jsonify, request
from app.models import User
from app import db
import re

user_bp = Blueprint('user_service', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    if 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Missing username or email'}), 400
    
    # Validate email format
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate username length
    if len(data['username']) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data:
        if len(data['username']) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        user.username = data['username']
        
    if 'email' in data:
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        user.email = data['email']
    
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user_id} deleted'})
