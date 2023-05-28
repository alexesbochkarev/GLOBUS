from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework import viewsets


from .models import Room
from .serializers import RoomListSerializer, RoomSerializer


User = get_user_model()


class RoomViewSet(viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def list(self, request, *args, **kwargs):
        room_list = Room.objects.filter(Q(user1=request.user) |
                                                    Q(user2=request.user))
        serializer = RoomListSerializer(instance=room_list, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        try:
            reciever = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': _('Собеседник не найден')})

        room = Room.objects.filter(Q(user1=request.user, user2=reciever) |
                                                    Q(user1=reciever, user2=request.user))
        if room.exists():
            return Response({'message': _('Диалог уже существует')})
        else:
            room = Room.objects.create(user1=request.user, user2=reciever)
            return Response(RoomSerializer(instance=room).data)
        