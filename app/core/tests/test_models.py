from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Tests Creating Users"""
        email = 'abdulrehman.ajmal@outlook.com'
        password = 'hello_999'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests Creating Users with normalized email"""
        email = 'oreo@OREO.com'
        user = get_user_model().objects.create_user(

            email=email,
            password='hello_999'
        )
        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Tests new users with invalid emails"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'hello_999')


    def test_new_user_is_superuser(self):
        """Test that user is a superuser"""
        email = 'abdulrehman.ajmal@outlook.com'
        password = 'hello_999'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)