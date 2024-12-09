from flask import Blueprint, request, jsonify
from app.models.member import Member, members
from app.models.book import books
from app.utils.auth import token_required
from datetime import datetime

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
@token_required
def get_members():
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Calculate slice indices
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get total count and sliced members
    total_members = len(members)
    page_members = list(members.values())[start:end]
    
    return jsonify({
        'members': [member.to_dict() for member in page_members],
        'total': total_members,
        'page': page,
        'per_page': per_page,
        'total_pages': (total_members + per_page - 1) // per_page
    })

@members_bp.route('/<int:member_id>', methods=['GET'])
@token_required
def get_member(member_id: int):
    member = members.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    return jsonify(member.to_dict())

@members_bp.route('/<int:member_id>', methods=['PUT'])
@token_required
def update_member(member_id: int):
    member = members.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    member.name = data.get('name', member.name)
    member.email = data.get('email', member.email)
    if 'password' in data:
        member.password_hash = Member.hash_password(data['password'])
    member.updated_at = datetime.now()
    
    return jsonify(member.to_dict())

@members_bp.route('/<int:member_id>', methods=['DELETE'])
@token_required
def delete_member(member_id: int):
    if member_id not in members:
        return jsonify({'message': 'Member not found'}), 404
    
    # Check if member has borrowed books
    member = members[member_id]
    if member.books_borrowed:
        return jsonify({
            'message': 'Cannot delete member with borrowed books',
            'borrowed_books': member.books_borrowed
        }), 400
    
    del members[member_id]
    return jsonify({'message': 'Member deleted successfully'})

@members_bp.route('/<int:member_id>/borrow/<int:book_id>', methods=['POST'])
@token_required
def borrow_book(member_id: int, book_id: int):
    member = members.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    book = books.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    if book.quantity <= 0:
        return jsonify({'message': 'Book is not available'}), 400
    
    if book_id in member.books_borrowed:
        return jsonify({'message': 'Book already borrowed by member'}), 400
    
    book.quantity -= 1
    member.books_borrowed.append(book_id)
    
    return jsonify({
        'message': 'Book borrowed successfully',
        'member': member.to_dict(),
        'book': book.to_dict()
    })

@members_bp.route('/<int:member_id>/return/<int:book_id>', methods=['POST'])
@token_required
def return_book(member_id: int, book_id: int):
    member = members.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    book = books.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    if book_id not in member.books_borrowed:
        return jsonify({'message': 'Book was not borrowed by member'}), 400
    
    book.quantity += 1
    member.books_borrowed.remove(book_id)
    
    return jsonify({
        'message': 'Book returned successfully',
        'member': member.to_dict(),
        'book': book.to_dict()
    })
