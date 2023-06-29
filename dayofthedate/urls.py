from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from daters.views import RegisterUserAPIView, AddToMatchView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/clients/create/', RegisterUserAPIView.as_view()),
    path('api/clients/<int:id>/match/',
         AddToMatchView.as_view(), name='add-to-match'),
]

urlpatterns += [
    path("api/clients/", include("rest_framework.urls")),
    path('api/auth/login/', obtain_auth_token, name='api-token-auth'),
]
