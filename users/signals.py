from django.dispatch import receiver
from django.dispatch import Signal
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from .models import Role
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()
user_registered = Signal()

# @receiver(user_registered, dispatch_uid="create_profile", sender=User)
# def create_profile(sender, user, request, **kwargs):
#     """Создаём профиль пользователя при регистрации"""
#     data = request.data

#     Role.objects.create(
#         user=user,
#         name=data.get("name", ""),
#         surname=data.get("surname", "")
#    )

# @receiver(pre_save, sender=User)
# def send_email(sender ,instance, request,*args ,**kwargs):
#     print(request.POST.get("password", ""), instance.email)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Создаём токен пользователя при регистрации"""
    if created:
        Token.objects.create(user=instance)
        Role.objects.create(
            user=instance,
        )
        send_mail(
            subject=f'Привет! {instance.email}',
            message=f'{instance.email}, {instance.password}',
            from_email='GLOBUS',
            recipient_list=[instance.email,]
        )