from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test The Users Api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test Creating user with payload"""
        payload = {'email': 'helo@world.com',
                   'name': 'heloworld!', 'password': 'testpass', }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user which already exists"""
        payload = {'email': 'helo@world.com',
                   'password': 'testpass', 'name': 'heloworld!', }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test creating a user with short password"""
        payload = {'email': 'helo@world.com',
                   'password': 'pa', 'name': 'heloworld!'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Token is created for user"""
        payload = {'email': 'helo@world.com', 'password': 'testpass', }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid(self):
        """Test token for invalid credentials"""
        payload = {'email': 'helo@world.com', 'password': 'wrongpass'}
        create_user(email='helo@world.com', password='testpass')
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """Test token when user is not created"""
        payload = {'email': 'helo@world.com', 'password': 'wrongpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field(self):
        """Test email and password is required"""
        payload = {'email': 'helo@world.com','password':''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

