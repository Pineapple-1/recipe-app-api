from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer


TAG_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):
    """Handels the tests for tags public api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Tests that the login is required for retriving the tags"""
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """Handels the authorized users for tags api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='helo@world.com', password='testpass')

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retriving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test the tags are returned to authenticated users"""
        imposter = get_user_model().objects.create_user(
            email='imposter@killer.com', password='im_an_imposter')
        Tag.objects.create(user=imposter, name='BAD_FOOD')
        tag = Tag.objects.create(user=self.user, name='fruit')
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tags_successfull(self):
        """Test creating new Tag"""
        payload = {'name': 'Test Tag'}
        self.client.post(TAG_URL, payload)
        exists = Tag.objects.filter(user=self.user, name = payload['name']).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating new tag invalid"""
        payload = {'name':''}
        res = self.client.post(TAG_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


