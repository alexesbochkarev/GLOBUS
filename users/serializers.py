from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from .models import User, Staff


class ProfileCreateSerializer(serializers.Serializer):
    surname = serializers.CharField()
    name = serializers.CharField()
    position = serializers.CharField()


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField()
    roles = serializers.ChoiceField(choices=User.Role.choices)
    pic = serializers.ImageField()
    visibleforchat = serializers.BooleanField()
    staff = ProfileCreateSerializer()


    def create(self, validated_data):
        staff_data = validated_data.pop('staff')
        user = User.objects.create_user(**validated_data)
        Staff.objects.create(user=user, **staff_data)
        return user


class UserListSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField()
    visibleforchat = serializers.BooleanField()
    roles = serializers.ChoiceField(choices=User.Role.choices)
    pic = serializers.ImageField()


class StaffCreateSerializer(serializers.Serializer):
    user = UserListSerializer()
    surname = serializers.CharField()
    name = serializers.CharField()
    position = serializers.CharField()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = User.objects.make_random_password()
        user = User.objects.create_user(password=password, **user_data)
        role =  Staff.objects.create(user=user, **validated_data)
        return role