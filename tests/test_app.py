import unittest
import sys
import os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from database import db
from models import Book, Customer, Loan

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.client = app.test_client()  
        with app.app_context():
            db.create_all()  

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Library Management System!', response.data)

    def test_add_book(self):
        book_data = {
            'title': '1984',
            'author': 'George Orwell',
            'year': 1949,
            'category': 'Dystopian',
            'available': True
        }
        response = self.client.post('/books/', json=book_data)
        self.assertEqual(response.status_code, 201)

        with app.app_context():
            book = Book.query.filter_by(title='1984').first()
            self.assertIsNotNone(book)
            self.assertEqual(book.author, 'George Orwell')

    def test_get_books(self):
        book_data = {
            'title': '1984',
            'author': 'George Orwell',
            'year': 1949,
            'category': 'Dystopian',
            'available': True
        }
        self.client.post('/books/', json=book_data)

        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1984', response.data)

    def test_add_customer(self):
        customer_data = {
            'name': 'John Doe',
            'city': 'New York',
            'age': 30
        }
        response = self.client.post('/customers/', json=customer_data)
        self.assertEqual(response.status_code, 201)

        with app.app_context():
            customer = Customer.query.filter_by(name='John Doe').first()
            self.assertIsNotNone(customer)
            self.assertEqual(customer.city, 'New York')

    def test_loan_book(self):
        with app.app_context():
            book = Book(title='1984', author='George Orwell', year=1949, category='Dystopian', available=True)
            customer = Customer(name='John Doe', city='New York', age=30)
            db.session.add(book)
            db.session.add(customer)
            db.session.commit()

        loan_data = {
            'customer_id': customer.id,
            'book_id': book.id,
            'loan_date': date(2024, 9, 25),
            'return_date': date(2024, 10, 2),
            'duration': 'EXTENDED'
        }
        response = self.client.post('/loans/', json=loan_data)
        self.assertEqual(response.status_code, 201)

        with app.app_context():
            loan = Loan.query.filter_by(customer_id=customer.id, book_id=book.id).first()
            self.assertIsNotNone(loan)

if __name__ == '__main__':
    unittest.main()