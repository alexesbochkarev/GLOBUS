from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import random
import string

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'password')


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        upass = ''.join(random.choice(string.ascii_letters + string.digits + '!@#$%^&*()_') for _ in range(10))
        user = User.objects.create_user(**validated_data, password=upass)
        return user

    class Meta:
        model = User
        exclude = (
            'password', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions',
            'last_login', 'date_joined',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})