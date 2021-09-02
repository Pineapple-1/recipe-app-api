from user.serializers import UserSerializer
from rest_framework import generics


class CreateUsersView(generics.CreateAPIView):
    """Creates new user in the system"""
    serializer_class = UserSerializer