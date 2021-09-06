from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """Tests the publicly avalible api"""

    def setUp(self):
        """Setup function"""
        self.client = APIClient()

    def test_login_required(self):
        """Test for login"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Test ingredients can be used by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='helo@world.com',
            password='testpass'
        )
        self.client.force_authenticate()

    def test_retrieve_ingredient_list(self):
        """Test retriving a list of ingredient"""

        Ingredient.objects.create(user=self.user, name="Kale")
        Ingredient.objects.create(user=self.user, name="Salt")
        res = self.client.get(INGREDIENT_URL)
        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """test that ingredients for authenticated user are returned"""

        imposter = get_user_model().objects.create_user(
            email='imposter@killer.com', password='im_an_imposter')
        Ingredient.objects.create(user=imposter, name="Kale")
        ingredient = Ingredient.objects.create(user=self.user, name="Salt")
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_CREATED)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'],ingredient.name)
