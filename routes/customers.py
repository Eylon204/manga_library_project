from flask import Blueprint, jsonify, request
from models import Customer
from database import db

customers_bp = Blueprint('customers', __name__)

# Add customer
@customers_bp.route('/customers', methods=['POST'])
def add_customer():
    data = request.json

    # Validate input data
    if not all(key in data for key in ['name', 'city', 'age']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_customer = Customer(
        name=data['name'],
        city=data['city'],
        age=data['age']
    )

    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add customer'}), 500

# Get customer by name
@customers_bp.route('/customers/get_customer_by_name/<string:name>', methods=['GET'])
def get_customer_by_name(name):
    customer = Customer.query.filter_by(name=name).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer.to_dict()), 200

# Update customer by name
@customers_bp.route('/customers/update_customer_by_name/<string:name>', methods=['PUT'])
def update_customer_by_name(name):
    customer = Customer.query.filter(Customer.name.ilike(f'%{name}%')).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.city = data.get('city', customer.city)
    customer.age = data.get('age', customer.age)
    
    db.session.commit()
    return jsonify(customer.to_dict()), 200

# Delete customer by name
@customers_bp.route('/customers/delete_customer_by_name/<string:name>', methods=['DELETE'])
def delete_customer_by_name(name):
    customer = Customer.query.filter(Customer.name.ilike(f'%{name}%')).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200   