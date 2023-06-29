from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import RegistrationSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
