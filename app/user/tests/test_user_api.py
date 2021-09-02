from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """Test The Users Api"""

    def setUp(self):
        self.client = APIClient()


    def test_create_valid_user_success(self):
        """Test Creating user with payload"""
        payload = {
            'email': 'test@oreo.com',
            'name':'oreo',
            'password':'testpass',
            
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        """Test creating a user which already exists"""
        payload = {
            'email': 'oreo@oreo.com',
            'password':'helo1234',
            'name':'oreo',
        }
        create_user(**payload) 
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test creating a user with short password"""
        payload = {
            'email': 'test@oreo.com',
            'password':'pw',
            'name' : 'oreo'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email = payload['email']).exists()
        self.assertFalse(user_exists)
