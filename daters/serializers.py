from rest_framework import serializers
from .models import DaterUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DaterUser
        fields = ['username', 'password', 'avatar',
                  'gender', 'first_name', 'last_name', 'email', 'longitude', 'latitude']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = DaterUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaterUser
        fields = ['longitude', 'latitude']


class DaterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaterUser
        fields = ['id', 'avatar', 'gender', 'first_name',
                  'last_name', 'email', 'longitude', 'latitude']
