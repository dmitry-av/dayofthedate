from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RegistrationSerializer
from django.core.mail import send_mail

from .utils.imageprocessing import add_watermark
from dayofthedate import settings

from daters.serializers import DaterUserSerializer
from daters.models import DaterUser


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # add watermark to user avatar
        watermark_avatar = add_watermark(user.avatar)
        user.avatar.save(user.avatar.name, watermark_avatar, save=True)


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
                    message=f"Вы понравились пользователю {target_user.username}! Email участника: {user.email}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[target_user.email],
                )

            return Response({'message': 'User added to match successfully.'})

        except DaterUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=404)


class MemberListAPIView(ListAPIView):
    queryset = DaterUser.objects.all()
    serializer_class = DaterUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'first_name', 'last_name']
