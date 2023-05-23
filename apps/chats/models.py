from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    user_sent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, 
                                    blank=True, related_name='thread_first_person')
    user_received = models.ForeignKey(User, on_delete=models.CASCADE, null=True, 
                                    blank=True, related_name='thread_second_person')
    
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, null=True, blank=True, 
                             on_delete=models.CASCADE, 
                             related_name='chatmessage_room')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)