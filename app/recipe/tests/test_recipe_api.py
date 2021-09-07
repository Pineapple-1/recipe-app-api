from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Creates a sample recipe"""
    default = {
        'title': 'steak burger',
        'time_minutes': '10',
        'price': '5.00'
    }
    default.update(params)
    return Recipe.objects.create(user=user, **default)


def detail_url(id):
    """Returns recipe id"""
    return reverse('recipe:recipe-detail', args=[id])


def sample_tag(user, name="Main course"):
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='peper'):
    return Ingredient.objects.create(user=user, name=name)


class PublicRecipeApiTest(TestCase):
    """Tests the publicly avalible api"""

    def setUp(self):
        """Setup function"""
        self.client = APIClient()

    def test_auth_required(self):
        """Test for login"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test Recipe cannot be used by authorized user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='helo@world.com', password='testpass')

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe_list(self):
        """Test retriving a list of Recipe"""

        sample_recipe(self.user)
        sample_recipe(self.user)
        res = self.client.get(RECIPE_URL)
        recipe = Recipe.objects.all()
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_limited_user(self):
        """Test retriving a list of Recipe for users"""
        imposter = get_user_model().objects.create_user(
            email='imposter@killer.com', password='im_an_imposter')
        sample_recipe(user=self.user)
        sample_recipe(user=imposter)

        res = self.client.get(RECIPE_URL)
        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_view_recipe_detail(self):

        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serializer.data)

    def test_creating_basic_recipe(self):
        payload = {
            'title': 'steak burger',
            'time_minutes': 10,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id= res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe,key))


    def test_create_recipe_with_tags(self):
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Non-Vegan')
        payload = {
            'title': 'steak burger',
            'tags' : [tag1.id,tag2.id],
            'time_minutes': 10,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(),2)
        self.assertIn(tag1,tags)
        self.assertIn(tag2,tags)
    
    def test_create_recipe_with_ingrediets(self):
        ingredient1 = sample_ingredient(user=self.user, name='chilli')
        ingredient2 = sample_ingredient(user=self.user, name='pepper')
        payload = {
            'title': 'steak burger',
            'ingredients' : [ingredient1.id,ingredient2.id],
            'time_minutes': 10,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        ingredient = recipe.ingredients.all()
        self.assertEqual(ingredient.count(),2)
        self.assertIn(ingredient1,ingredient)
        self.assertIn(ingredient2,ingredient)
    
