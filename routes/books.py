from flask import Blueprint, logging, request, jsonify
from database import db
from models import Book

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/books/', methods=['POST'])
def add_book():
    data = request.get_json()
    print("Received data:", data)  # Print received data
    
    if not data or 'title' not in data or 'author' not in data or 'year' not in data or 'category' not in data:
        print("Missing required fields")  # Log for missing fields
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Attempt to convert year to integer
    try:
        year = int(data['year'])
    except ValueError:
        return jsonify({'message': 'Year must be a valid integer'}), 400
    
    # Validate year is a positive number
    if year <= 0:
        print("Year must be a positive number") 
        return jsonify({'message': 'Year must be a positive number'}), 400

    try:
        new_book = Book(
            title=data['title'],
            author=data['author'],
            year=year, 
            category=data['category'],
            available=data.get('available', True)
        )
        db.session.add(new_book)
        db.session.commit()
        print("Book added successfully")  
        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        print(f"Error adding book: {e}") 
        return jsonify({'message': 'Failed to add book'}), 500
        
@book_bp.route('/books/get_book_by_title/<string:title>', methods=['GET'])
def get_book_by_title(title):
    book = Book.query.filter_by(title=title).first() 
    if book:
        return jsonify(book.to_dict()), 200  
    else:
        return jsonify({'error': 'Book not found'}), 404 

@book_bp.route('/books/get_all', methods=['GET'])
def get_all_books():
    books = Book.query.all()  # מחפש את כל הספרים במסד הנתונים
    return jsonify([book.to_dict() for book in books]), 200  # מחזיר את כל הספרים במבנה JSON

@book_bp.route('/books/update_book_by_title/<string:title>', methods=['PUT'])
def update_book_by_title(title):
    book = Book.query.filter_by(title=title).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

@book_bp.route('/books/delete_book_by_title/<string:title>', methods=['DELETE'])
def delete_book_by_title(title):
    book = Book.query.filter_by(title=title).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200