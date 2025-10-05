import json
from api.utils.test_base import BaseTestCase
from api.models.users import User
from datetime import datetime
import unittest
from api.utils.token import generate_token, verify_token


def create_users():
    user1 = User(username="walehhhh", email="walehh@gmail.com", password=User.generate_hash("helloworld"), verified=True).create()
    user2 = User(username="bitch", email="bitch@yahoo.com", password=User.generate_hash("bitchyyyy")).create()


class TestUsers(BaseTestCase):
    def setUp(self):
        super().setUp()
        create_users()
    
    def test_valid_login(self):
        user = {
            "email": "walehh@gmail.com",
            "username": "walehhhh",
            "password": "helloworld"
        }

        response = self.app.post('/api/users/login', data=json.dumps(user), content_type ='application/json')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in data)

    def test_invalid_login(self):
        user = {
            "email": "walehh@gmail.com",
            "username": "walehhhh",
            "password": "wrongpass"
        }

        response = self.app.post('api/users/login', data=json.dumps(user), content_type ='application/json')
        data = json.loads(response.data)
        self.assertEqual(403, response.status_code)
    
    def test_unverified_login(self):
        user = {
            "email": "bitch@yahoo.com",
            "username": "bitch",
            "password": "bitchyyyy",
        }

        response = self.app.post('api/users/login', data=json.dumps(user), content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)

    def test_correct_verify_email(self):
        token = generate_token("bitch@yahoo.com")
        response = self.app.get(f'/api/users/confirm/{token}', content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)

    def test_incorrect_verify_email(self):
        token = generate_token("bitchy@yahoo.com")
        response = self.app.get(f"/api/users/confirm/{token}", content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    unittest.main()
