from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Room(models.Model):
    user1 = models.ForeignKey(User, 
                              on_delete=models.SET_NULL, 
                              null=True, related_name='sender', 
                              db_index=True)
    user2 = models.ForeignKey(User, 
                              on_delete=models.SET_NULL, 
                              null=True, 
                              related_name='receiver', 
                              db_index=True)
    
    start_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return _("Chats between ") + f"{self.user1.email}, {self.user2.email}"


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='message_sender')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=200)
    attachment = models.FileField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.author} {self.room})"

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")




