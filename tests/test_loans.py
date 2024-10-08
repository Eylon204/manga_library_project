import unittest
import sys
import os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from database import db
from models import Loan, Customer, Book

class LoanTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

        with app.app_context():
            db.create_all()

    def setUp(self):
        with app.app_context():
            customer = Customer(name='Jane Smith', city='Loan City', age=28)
            book = Book(title='Loan Test Book', author='Loan Test Author', year=2020, available=True)
            db.session.add(customer)
            db.session.add(book)
            db.session.commit()

            self.customer_id = customer.id
            self.book_id = book.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_loan(self):
        response = self.app.post('/loans', json={
            'customer_id': self.customer_id,
            'book_id': self.book_id,
            'loan_date': str(date.today()),
            'return_date': None
        })
        self.assertEqual(response.status_code, 201)

    def test_get_loan_by_id(self):
        loan = Loan(customer_id=self.customer_id, book_id=self.book_id, loan_date=date.today())
        db.session.add(loan)
        db.session.commit()

        response = self.app.get(f'/loans/{loan.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_loan(self):
        loan = Loan(customer_id=self.customer_id, book_id=self.book_id, loan_date=date.today())
        db.session.add(loan)
        db.session.commit()

        response = self.app.put(f'/loans/{loan.id}', json={
            'return_date': str(date.today())
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()