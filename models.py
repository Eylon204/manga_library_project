from enum import Enum
from flask_login import UserMixin
from database import db

class LoanDuration(Enum):
    VERY_SHORT = "for 2 days"
    CUSTOM = "for 5 days"
    EXTENDED = "for 10 days"

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'user'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    loans = db.relationship('Loan', backref='user', lazy=True)

# Customer model
class Customer(db.Model):
    __tablename__ = 'customer' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'city': self.city,
            'user_id': self.user_id 
        }

# Book model
class Book(db.Model):
    __tablename__ = 'book' 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'category': self.category,
            'available': self.available,
        }
            
# Loan model
class Loan(db.Model):
    __tablename__ = 'loan' 
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)  # Changed to nullable=True
    duration = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'book_id': self.book_id,
            'user_id': self.user_id,  
            'loan_date': self.loan_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'duration': self.duration 
        }