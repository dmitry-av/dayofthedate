from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import RegistrationSerializer, DaterUserSerializer, UpdateUserSerializer
from .utils.imageprocessing import add_watermark
from .filters import DistanceFilterBackend
from daters.models import DaterUser


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # add watermark to user avatar
        watermark_avatar = add_watermark(user.avatar)
        user.avatar.save(user.avatar.name, watermark_avatar, save=True)


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.get_object()
        avatar = serializer.validated_data.get('avatar')
        if avatar:
            watermark_avatar = add_watermark(avatar)
            user.avatar.save(avatar.name, watermark_avatar, save=True)
            serializer.validated_data.pop('avatar', None)
        return super().perform_update(serializer)


class AddToMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = self.request.user
        try:
            target_user = DaterUser.objects.get(id=id)
        except DaterUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=404)
        user.match.add(target_user)
        return Response({'message': 'User added to match successfully.'})


class MemberListAPIView(ListAPIView):
    queryset = DaterUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DaterUserSerializer
    filter_backends = [DjangoFilterBackend, DistanceFilterBackend]
    filterset_fields = ['gender', 'first_name', 'last_name']
