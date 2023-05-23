from rest_framework import serializers
from django.contrib.auth import get_user_model
# from model_utils.models import TimeStampedModel, SoftDeletableModel
from .models import Room, Message

User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ["password"]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone",]



class MessageSerializer(serializers.ModelSerializer):
    timestamp_formatted = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_timestamp_formatted(self, obj: Message):
        return obj.timestamp.strftime("%d-%m-%Y %H:%M:%S")


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["pk", "user1", "messages", "user2", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj: Room):
        return MessageSerializer(obj.messages.order_by('timestamp').last()).data


