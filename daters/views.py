from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail

from dayofthedate import settings
from .serializers import RegistrationSerializer, DaterUserSerializer, UpdateLocationSerializer
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


class UpdateUserLocationView(generics.UpdateAPIView):
    serializer_class = UpdateLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddToMatchView(APIView):
    def post(self, request, id):
        try:
            user = self.request.user
            target_user = DaterUser.objects.get(id=id)
            if user.match.filter(id=target_user.id).exists():
                return Response({'message': 'User is already your match'}, status=400)

            user.match.add(target_user)

            if target_user.match.filter(id=user.id).exists():
                # send email notification to both users
                send_mail(
                    subject='Взаимная симпатия',
                    message=f"Вы понравились пользователю {target_user.username}! Email участника: {target_user.email}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                send_mail(
                    subject='Взаимная симпатия',
                    message=f"Вы понравились пользователю {user.username}! Email участника: {user.email}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[target_user.email],
                )

            return Response({'message': 'User added to match successfully.'})

        except DaterUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=404)


class MemberListAPIView(ListAPIView):
    queryset = DaterUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DaterUserSerializer
    filter_backends = [DjangoFilterBackend, DistanceFilterBackend]
    filterset_fields = ['gender', 'first_name', 'last_name']
