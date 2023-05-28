from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField
from sequences import get_next_value

from .managers import UserManager, MemberManager


class User(AbstractBaseUser, PermissionsMixin):
    """AbstractCustomUser
    """ 
    class Role(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin  
        MEMBER   = '1', _('Member')
        OBSERVER = '2', _('Observer')
        MANAGER  = '3', _('Manager')
        ADMIN    = '4', _('Administrator')

    username = None
    email      = models.EmailField(_('email address'), unique=True)
    phone      = PhoneNumberField(_('phone number'), unique=True)
    surname    = models.CharField(_("first name"), max_length=150, blank=True)
    name       = models.CharField(_("last name"), max_length=150, blank=True)
    patronymic = models.CharField(_("patronymic"), max_length=150, blank=True)
    position   = models.CharField(_("position"), max_length=150, blank=True)
    role        = models.CharField(_("role"), max_length=1, choices=Role.choices, default='1')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    avatar      = models.ImageField(
                                upload_to='user_pic', 
                                height_field=None,
                                width_field=None, 
                                null=True, blank=True
                            )
    is_staff    = models.BooleanField(
                                _("staff status"),
                                default=False,
                                help_text=_("Designates whether the user can log into this admin site."),
                            )
    is_active   = models.BooleanField(
                                _("active"),
                                default=True,
                                help_text=_(
                                    "Designates whether this user should be treated as active. "
                                    "Unselect this instead of deleting accounts."
                                ),
                            )
    # Fields for staff
    visibleforchat = models.BooleanField(_("visible for chat"), default=True)
    visibleformembers = models.BooleanField(_("visible for members"), default=True)

    # Fields for member
    score       = models.PositiveIntegerField(_('Score'), default=0)
    money       = models.PositiveIntegerField(_('Money'), default=0)
    device      = models.CharField(_('Device'), max_length=150, null=True, blank=True)
    loyaltyCard = models.CharField(
                                _('Loyalty card'), 
                                max_length=10, 
                                default=get_next_value("loyalty card")
                            )

    objects = UserManager()
    members = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('email', 'phone')

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
    


