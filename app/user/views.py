from user.serializers import UserSerializer,AuthTokenSerialzer
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings



class CreateUsersView(generics.CreateAPIView):
    """Creates new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Generates Token for the user"""
    serializer_class = AuthTokenSerialzer
    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES