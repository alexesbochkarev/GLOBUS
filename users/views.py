from rest_framework import viewsets, mixins, status, views, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.mail import send_mail

from .models import User
from .models import Staff
#from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, PasswordResetSerializer, RoleCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsUserOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "set_password":
            return PasswordResetSerializer

        return self.serializer_class

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        phone = serializer.data["phone"]
        user = User.objects.filter(email=email, phone=phone)
        serializer.user.password(serializer.data["password"])
        serializer.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCreateViewSet(viewsets.ModelViewSet):
    """
    Creates user accounts
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

        # email=serializer.data["email"]
        upass = User.objects.make_random_password()
        serializer.save(password=upass)
        headers = self.get_success_headers(serializer.data)
        # email=serializer.data["email"]
        # send_mail(
        #     subject=f'Привет! {email}',
        #     message=f'{email}, {serializer.data["password"]}',
        #     from_email='GLOBUS',
        #     recipient_list=[email,]
        # )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class RoleCreateViewSet(viewsets.ModelViewSet):
    """
    Creates user accounts
    """
    queryset = Staff.objects.all()
    serializer_class = RoleCreateSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "create":
            return RoleCreateSerializer
        return self.serializer_class