import base64

from django.db import models
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


from .models import User


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
    
    
class Role(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin  
        # 1 == member default value
        OBSERVER = '2', _('Observer')
        MANAGER  = '3', _('Manager')
        ADMIN    = '4', _('Administrator')


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Создание пользователя админки согласно ТЗ стр.93

    Пароль пользователя автоматичски генерируется во views.py 
    и отправляется на почту пользователя в письме-приглашении
    """
    id = serializers.ReadOnlyField()
    email = serializers.EmailField()
    phone = PhoneNumberField(region="RU")
    role = serializers.ChoiceField(choices=Role.choices)
    avatar = Base64ImageField(required=False, allow_null=True)
    surname = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    patronymic = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    visibleforchat = serializers.BooleanField()


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ["id", "email", "phone", "role", "avatar", "surname", "name", "patronymic", "position", "visibleforchat"]
        

