
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email='helo@world.com', password='testpass'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email,password)


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

        user = get_user_model().objects.create_superuser(
            'abdulrehman.ajmal@outlook.com',
            'hello_999'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_tag_str(self):
        """tests the tag representation"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan'
        )
        self.assertEqual(str(tag),tag.name)
    
    def test_ingredient_str(self):
        """tests the ingredient representation"""
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'Cucumber'
        )
        self.assertEqual(str(ingredient),ingredient.name)
    
    def test_Recipe_str(self):
        """tests the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'steak',
            time_minutes = '5',
            price = '5.00'
        )
        self.assertEqual(str(recipe),recipe.title)
    
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that the recipe image has a correct filename"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None,'myfile.jpg')  
        exp_path = f'uploads/recipe/{uuid}.jpg'  
        self.assertEqual(file_path,exp_path)


    