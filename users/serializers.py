from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'password')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class MyKeywordsField(serializers.RelatedField):
    def to_native(self, value):
        return { str(value.pk): value.name }

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField()
    is_staff = serializers.BooleanField()
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # class Meta:
    #     model = User
    #     fields = ('id', 'email', 'phone')
        # exclude = (
        #     'password', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions',
        #     'last_login', 'date_joined',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})