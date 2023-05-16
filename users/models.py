import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=30, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    visibleforchat = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date join'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('email', 'phone')

    def __str__(self):
        return f"{self.email}"
    

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    surname = models.CharField(_("first name"), max_length=150, blank=True)
    name = models.CharField(_("last name"), max_length=150, blank=True)
    patronymic = models.CharField(_("patronymic"), max_length=150, blank=True)
    position = models.CharField(_("position"), max_length=150, blank=True)
    pic = models.ImageField(
        upload_to='user_pic', 
        height_field=None, width_field=None, max_length=100, blank=True)
    
    class Meta:
        verbose_name = _('Персонал')
        verbose_name_plural = _('Персонал')

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic} | {self.user.email} | {self.user.phone}"

