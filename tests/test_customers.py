import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from database import db
from models import Customer

class CustomerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_customer(self):
        response = self.app.post('/customers/', json={
            'name': 'John Doe',
            'city': 'Test City',
            'age': 30
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['city'], 'Test City')

    def test_get_customer_by_name(self):
        self.test_add_customer()

        response = self.app.get('/customers/get_customer_by_name/John%20Doe')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'John Doe')

    def test_update_customer(self):
        self.test_add_customer()

        response = self.app.put('/customers/update_customer_by_name/John%20Doe', json={
            'city': 'Updated City',
            'age': 35
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['city'], 'Updated City')
        self.assertEqual(data['age'], 35)

    def test_delete_customer(self):
        self.test_add_customer()

        response = self.app.delete('/customers/delete_customer_by_name/John%20Doe')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Customer deleted successfully', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()