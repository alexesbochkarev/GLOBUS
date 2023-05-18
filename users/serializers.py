from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from .models import User, Staff


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
    

class ProfileCreateSerializer(serializers.Serializer):
    surname = serializers.CharField()
    name = serializers.CharField()
    position = serializers.CharField()


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField()
    is_staff = serializers.BooleanField()
    roles = serializers.ChoiceField(choices=User.Role.choices)
    pic = serializers.ImageField()
    staff = ProfileCreateSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'is_staff', 'roles', 'pic', 'staff',]

    def create(self, validated_data):
        staff_data = validated_data.pop('staff')
        user = User.objects.create_user(**validated_data)
        Staff.objects.create(user=user, **staff_data)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})


class UserListSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField()
    visibleforchat = serializers.BooleanField()
    roles = serializers.ChoiceField(choices=User.Role.choices)
    pic = serializers.ImageField()


class RoleCreateSerializer(serializers.Serializer):
    user = UserListSerializer()
    surname = serializers.CharField()
    name = serializers.CharField()
    position = serializers.CharField()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = User.objects.make_random_password()
        user = User.objects.create_user(password=password, is_staff=True, **user_data)
        role =  Staff.objects.create(user=user, **validated_data)
        return role