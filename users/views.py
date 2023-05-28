from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.mail import send_mail

from .models import User
from .serializers import CreateUserSerializer

User = get_user_model()



class UserCreateViewSet(viewsets.ModelViewSet):
    """
    Create user-staff accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = User.objects.make_random_password()
        serializer.save(password=password)

        # Отправляем письмо с логином и паролем на почту пользователя
        email=serializer.data["email"]
        send_mail(
            subject=f'Привет! {email}',
            message=f'Ваши учётные данные: \n логин: {email} \n пароль: {password}',
            from_email='noreply@refocus.community',
            recipient_list=[email,]
        )
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
