import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from database import db
from models import Book

class BookTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

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

    def test_add_book(self):
        response = self.app.post('/books/', json={
            'title': '1984',
            'author': 'George Orwell',
            'year': 1949,
            'category': 'Dystopian',
            'available': True
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('1984', response.get_data(as_text=True))

    def test_get_book_by_title(self):
        self.test_add_book()

        response = self.app.get('/books/get_book_by_title/1984')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1984', response.get_data(as_text=True))

    def test_update_book(self):
        self.test_add_book()

        response = self.app.put('/books/update_book_by_title/1984', json={
            'author': 'Eric Blair',
            'year': 1950
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Eric Blair', response.get_data(as_text=True))

    def test_delete_book(self):
        self.test_add_book()

        response = self.app.delete('/books/delete_book_by_title/1984')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book deleted successfully', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()