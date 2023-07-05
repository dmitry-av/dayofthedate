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


class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = DaterUser
        fields = ['longitude', 'latitude', 'avatar',
                  'first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class DaterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaterUser
        fields = ['id', 'avatar', 'gender', 'first_name',
                  'last_name', 'email', 'longitude', 'latitude']
