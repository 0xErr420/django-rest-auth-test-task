from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class TestUserRegistrationView(APITestCase):
    route = '/api/auth/register/'
    def test_user_registration_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(self.route, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'User created successfully.'})

    def test_user_registration_failure(self):
        response = self.client.post(self.route, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestUserChangeLoginView(APITestCase):
    route = '/api/auth/change-login/'

    def setUp(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        data_2 = {
            'username': 'Tom',
            'password': 'testpassword',
            'email': 'tom@example.com'
        }
        # Register first user and get token
        self.client.post('/api/auth/register/', data, format='json')
        self.tokens = self.client.post('/api/auth/token/', data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens.json().get('access'))
        # Register second user
        self.client.post('/api/auth/register/', data_2, format='json')

    def test_user_change_login_success(self):
        data = {
            'new_username':'newtestusername'
        }
        response = self.client.post(self.route, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Username changed successfully.'})

    def test_user_change_login_failure_username_taken(self):
        data = {
            'new_username':'Tom'
        }
        response = self.client.post(self.route, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'The new username is already taken. Please choose another.'})

    def test_user_change_login_failure_same_username(self):
        data = {
            'new_username':'testuser'
        }
        response = self.client.post(self.route, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'New username cannot be the same as the current username.'})


