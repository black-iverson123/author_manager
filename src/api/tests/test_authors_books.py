import json
from api.utils.test_base import BaseTestCase
from api.models.books import Book
from api.models.authors import Author
from datetime import datetime
import unittest
from flask_jwt_extended import create_access_token
import io


def create_authors_and_books():
    author1 = Author(first_name="Ben", last_name="Tennyson").create()
    Book(title="The Great Adventure", year=datetime(2019,6,1), edition="5th", author_id=author1.id).create()
    Book(title="Count of monte cristo", year=datetime(2008,3, 8), edition="First", author_id=author1.id).create()
    author2 = Author(first_name="Gwen", last_name="Tennyson").create()
    Book(title="Life is hard", year=datetime(2014,7,9), author_id=author2.id, edition="3rd").create()
    Book(title="Teenage Mutant Ninja turtles", year=datetime(2012,12, 12), author_id=author1.id, edition="4th").create()


def login():
    access_token = create_access_token(identity="maxwell@gmail.com")
    return access_token

class TestAuthorsBooks(BaseTestCase):
    def setUp(self):
        super().setUp()
        create_authors_and_books()
    
    def test_create_author(self):
        access_token = login()
        author = {
            "first_name": "Kevin",
            "last_name": "Levin"
        }

        response = self.app.post('/api/authors/', data=json.dumps(author), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('author' in data)

    def test_create_author_no_auth(self):
        author = {
            "first_name": "Dwayne",
            "last_name": "Johnson"
        }

        response = self.app.post('/api/authors/', data=json.dumps(author), content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
    
    def test_create_author_invalid_data(self):
        access_token = login()
        author = {
            "first_name": "Johnson"
        }
        response = self.app.post('/api/authors/', data=json.dumps(author), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
    
    def test_get_authors(self):
        response = self.app.get('/api/authors/', content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('authors' in data)
    
    def test_get_author_by_id(self):
        response = self.app.get('/api/authors/1', content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("author" in data)
    
    def test_get_author_by_wrong_id(self):
        response = self.app.get('/api/authors/29', content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        #self.assertTrue("author" in data)
    
    def test_update_author(self):
        access_token = login()
        author = {
            "first_name": "Diana",
            "last_name": "Prince"
        }

        response = self.app.put('/api/authors/2', data=json.dumps(author), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('author' in data)
    
    def test_modify_author(self):
        access_token = login()
        author = {
            "first_name": "Nina",
        }

        response = self.app.patch('/api/authors/1', data=json.dumps(author), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('author' in data)
    
    def test_upload_avatar(self):
        access_token = login()
        image = {
            "avatar": (io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"), "test_file.png")
        }
        response = self.app.post("/api/authors/avatar/2", data=image, content_type="multipart/form-data", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('avatar' in data)
    
    def test_upload_avatar_csv(self):
        access_token = login()
        response = self.app.post('/api/authors/avatar/2', data=dict(avatar=(io.BytesIO(b'test'), 'test_file.csv')), content_type="multipart/form-data", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
        

    def test_delete_author(self):
        access_token = login()
        response = self.app.delete('/api/authors/2', content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        #data = json.loads(response.data)
        self.assertEqual(204, response.status_code)
    
    
    def test_create_book(self):
        access_token = login()
        book = {
            "title": "Full Metal Alchemist",
            "year": "2003-10-04",
            "edition": "1st",
            "author_id": 1
        }

        response = self.app.post('/api/books/', data=json.dumps(book), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('book' in data)
    
    def test_create_book_no_auth(self):
        book = {
            "title": "Russian roulette",
            "year": "1986-11-04",
            "edition": "1st",
            "author_id": 1
        }

        response = self.app.post('/api/books/', data=json.dumps(book), content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
    
    def test_create_book_no_author(self):
        access_token = login()
        book = {
            "title": "Alice in wonderland",
            "year": "1865-11-26",
            "edition": "1st"
        }

        response = self.app.post('/api/books/', data=json.dumps(book), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
    
    def test_get_books(self):
        response = self.app.get('/api/books/', content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('books' in data)
    
    def get_specfic_book(self):
        response = self.app.get('/api/books/1', content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('book' in data)
    
    def test_wrong_book_id(self):
        response = self.app.get('/api/books/29', content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
    
    def test_update_book(self):
        access_token = login()
        book = {
            'title': "The Great Adventure",
            'year': "1988-05-01",
            'edition': "5th"
        }
        response = self.app.put('/api/books/1', data=json.dumps(book), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
    
    def test_update_book_wrong_id(self):
        access_token = login()
        book = {
            'title': "The Great Adventure",
            'year': "1988-05-01",
            'edition': "5th"
        }
        response = self.app.put('/api/books/29', data=json.dumps(book), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
    
    def test_modify_book(self):
        access_token = login()
        book = {
            'edition': "6th"
        }
        response = self.app.patch('/api/books/1', data=json.dumps(book), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
    
    def test_modify_book_wrong_id(self):
        access_token = login()
        book = {
            'edition': "6th"
        }
        response = self.app.patch('/api/books/14', data=json.dumps(book), content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
    
    def test_delete_book(self):
        access_token = login()
        response = self.app.delete('/api/books/1', content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(204, response.status_code)
    
    def test_delete_book_wrong_id(self):
        access_token = login()
        response = self.app.delete('/api/books/71', content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(404, response.status_code)



if __name__ == "__main__":
    unittest.main()