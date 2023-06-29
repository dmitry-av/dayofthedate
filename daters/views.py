from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import RegistrationSerializer

from .utils.imageprocessing import add_watermark


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # add watermark to user's avatar
        watermark_avatar = add_watermark(user.avatar)
        user.avatar.save(user.avatar.name, watermark_avatar, save=True)
