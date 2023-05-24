import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class AbstractCustomUser(AbstractBaseUser, PermissionsMixin):
    """""" 
    username = None
    email      = models.EmailField(_('email address'), unique=True)
    phone      = PhoneNumberField(_('phone number'), unique=True)
    surname    = models.CharField(_("first name"), max_length=150, blank=True)
    name       = models.CharField(_("last name"), max_length=150, blank=True)
    patronymic = models.CharField(_("patronymic"), max_length=150, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    pic        = models.ImageField(
                                upload_to='user_pic', 
                                height_field=None,
                                width_field=None, 
                                null=True, blank=True
                            )
    is_staff   = models.BooleanField(
                                _("staff status"),
                                default=False,
                                help_text=_("Designates whether the user can log into this admin site."),
                            )
    is_active  = models.BooleanField(
                                _("active"),
                                default=True,
                                help_text=_(
                                    "Designates whether this user should be treated as active. "
                                    "Unselect this instead of deleting accounts."
                                ),
                            )


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('email', 'phone')
        abstract = True

    def __str__(self):
        return f"{self.email}"
    
    def get_full_name(self):
        return f"{self.surname} {self.name} {self.patronymic}"
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    

class User(AbstractCustomUser):
    """
    Staff for CMS
    """
    class Role(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin  
        OBSERVER = 'Observer', _('Observer')
        MANAGER  = 'Manager', _('Manager')
        ADMIN    = 'Administrator', _('Administrator')

    role          = models.CharField(_("role"), choices=Role.choices)
    visibleforchat = models.BooleanField(_("visible for chat"), default=False)
    visibleformember = models.BooleanField(_("visible for member"), default=False)





# class Staff(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff'
#     )
#     surname = models.CharField(_("first name"), max_length=150, blank=True)
#     name = models.CharField(_("last name"), max_length=150, blank=True)
#     patronymic = models.CharField(_("patronymic"), max_length=150, blank=True)
#     position = models.CharField(_("position"), max_length=150, blank=True)
    
    
#     class Meta:
#         verbose_name = _('Персонал')
#         verbose_name_plural = _('Персонал')

#     def __str__(self):
#         return f"{self.surname} {self.name} | {self.user.email} | {self.user.phone}"

