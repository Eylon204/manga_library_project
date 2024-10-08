from flask import Blueprint, request, jsonify
from database import db
from models import Loan, Customer, Book
from flask_login import current_user
from datetime import date, timedelta

loans_bp = Blueprint('loans_bp', __name__)

@loans_bp.route('/loans', methods=['POST'])
def create_loan():
    data = request.get_json()

    # Make sure the user is logged in
    if current_user.is_authenticated:
        if not all(key in data for key in ['customer_id', 'book_id', 'loan_date', 'duration']):
            return jsonify({'error': 'Missing required fields'}), 400 

        try:
            loan_date = date.fromisoformat(data['loan_date'])  
        except ValueError:
            return jsonify({'error': 'Invalid loan_date format. Use YYYY-MM-DD.'}), 400

        # Determining the return date according to the duration of the loan
        if data['duration'] == 'VERY_SHORT':
            return_date = loan_date + timedelta(days=2)
        elif data['duration'] == 'CUSTOM':
            return_date = loan_date + timedelta(days=5)
        elif data['duration'] == 'EXTENDED':
            return_date = loan_date + timedelta(days=10)
        else:
            return jsonify({'error': 'Invalid duration provided.'}), 400

        new_loan = Loan(
            customer_id=data['customer_id'],
            book_id=data['book_id'],
            user_id=current_user.id, 
            loan_date=loan_date,
            return_date=return_date,
            duration=data['duration']
        )
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({'message': 'Loan created successfully!'}), 201
    else:
        return jsonify({'message': 'User not authenticated.'}), 401
            
# Update a loan by customer name and book title (return a book)
@loans_bp.route('/loans', methods=['PUT'])
def update_loan():
    data = request.get_json()

    if not all(key in data for key in ['customer_name', 'book_title']):
        return jsonify({'error': 'Missing required fields: customer_name and book_title are required'}), 400

    customer = Customer.query.filter_by(name=data['customer_name']).first()
    if not customer:
        return jsonify({'error': f'Customer with name {data["customer_name"]} not found'}), 404

    book = Book.query.filter_by(title=data['book_title']).first()
    if not book:
        return jsonify({'error': f'Book with title {data["book_title"]} not found'}), 404

    # Find the loan for this customer and book
    loan = Loan.query.filter_by(customer_id=customer.id, book_id=book.id).first()
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    try:
        # Update the loan's return date and mark the book as available
        loan.return_date = date.today()  
        book.available = True  
        db.session.commit()

        return jsonify({'message': 'Loan updated successfully', 'loan': loan.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update loan: {str(e)}'}), 500

# Search for a loan by customer name and book title
@loans_bp.route('/loans/search', methods=['GET'])
def get_loan():
    customer_name = request.args.get('customer_name')
    book_title = request.args.get('book_title')

    if not customer_name or not book_title:
        return jsonify({'error': 'Both customer_name and book_title are required'}), 400

    customer = Customer.query.filter_by(name=customer_name).first()
    if not customer:
        return jsonify({'error': f'Customer with name {customer_name} not found'}), 404

    book = Book.query.filter_by(title=book_title).first()
    if not book:
        return jsonify({'error': f'Book with title {book_title} not found'}), 404

    loan = Loan.query.filter_by(customer_id=customer.id, book_id=book.id).first()
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    return jsonify(loan.to_dict()), 200