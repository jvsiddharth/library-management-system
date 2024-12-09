from flask import Blueprint, request, jsonify
from app.models.member import Member, members
from app.utils.auth import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if email already exists
    if any(member.email == data['email'] for member in members.values()):
        return jsonify({'message': 'Email already registered'}), 400
    
    # Create new member
    member_id = len(members) + 1
    data['id'] = member_id
    member = Member.from_dict(data)
    members[member_id] = member
    
    return jsonify({
        'message': 'Member registered successfully',
        'member': member.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not all(field in data for field in ['email', 'password']):
        return jsonify({'message': 'Missing email or password'}), 400
    
    # Find member by email
    member = next((m for m in members.values() if m.email == data['email']), None)
    if not member or not member.verify_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # Generate token
    token = generate_token(member.id)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'member': member.to_dict()
    })
