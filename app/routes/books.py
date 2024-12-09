from flask import Blueprint, request, jsonify
from typing import Dict, List
from app.models.book import Book, books
from app.utils.auth import token_required
from datetime import datetime

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
@token_required
def get_books():
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Calculate slice indices
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get total count and sliced books
    total_books = len(books)
    page_books = list(books.values())[start:end]
    
    return jsonify({
        'books': [book.to_dict() for book in page_books],
        'total': total_books,
        'page': page,
        'per_page': per_page,
        'total_pages': (total_books + per_page - 1) // per_page
    })

@books_bp.route('/<int:book_id>', methods=['GET'])
@token_required
def get_book(book_id: int):
    book = books.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify(book.to_dict())

@books_bp.route('/', methods=['POST'])
@token_required
def create_book():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'author', 'isbn', 'quantity']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Create new book
    book_id = len(books) + 1
    data['id'] = book_id
    book = Book.from_dict(data)
    books[book_id] = book
    
    return jsonify(book.to_dict()), 201

@books_bp.route('/<int:book_id>', methods=['PUT'])
@token_required
def update_book(book_id: int):
    book = books.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.quantity = data.get('quantity', book.quantity)
    book.updated_at = datetime.now()
    
    return jsonify(book.to_dict())

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(book_id: int):
    if book_id not in books:
        return jsonify({'message': 'Book not found'}), 404
    
    del books[book_id]
    return jsonify({'message': 'Book deleted successfully'})

@books_bp.route('/search', methods=['GET'])
@token_required
def search_books():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'message': 'Search query is required'}), 400
    
    # Search by title or author
    results = [
        book.to_dict() for book in books.values()
        if query in book.title.lower() or query in book.author.lower()
    ]
    
    return jsonify({
        'results': results,
        'count': len(results)
    })
