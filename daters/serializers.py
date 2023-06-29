from rest_framework import serializers
from .models import DaterUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DaterUser
        fields = ['username', 'password', 'avatar',
                  'gender', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = DaterUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
