from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Room, Message


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "surname"]
        read_only_fields = ("name", "surname")


class AuthorSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    role = serializers.StringRelatedField()
            

class MessageSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Message
        exclude = ('room',)


class RoomListSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['user1', 'user2', 'last_message']

    def get_last_message(self, instance):
        message = instance.messages.first()
        if message:
            return MessageSerializer(instance=message).data
        else:
            return None


class RoomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()
    messages = MessageSerializer(read_only=True ,many=True)

    class Meta:
        model = Room
        fields = ['user1', 'user2', 'messages']
        read_only_fields = ('user1', 'user2', 'messages')
