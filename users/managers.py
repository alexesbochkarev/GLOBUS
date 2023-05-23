from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, phone=None,\
        password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        
        if not email and not phone:
            raise ValueError('The given email/phone must be set')

        user = self.model(
            email=email,
            phone=phone,
            **extra_fields
        )
        
        # проверяем является ли пользователь
        # суперпользователем
        if extra_fields.get('is_superuser'):
            user = self.model(
                email=email,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, \
                     password=None, **extra_fields):
        
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email , password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email=email,
            password=password,
            **extra_fields
        )