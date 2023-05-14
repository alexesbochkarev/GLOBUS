from rest_framework import viewsets, mixins, status, views, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
#from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, PasswordResetSerializer


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


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)