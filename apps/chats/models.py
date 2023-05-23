from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# from model_utils.models import TimeStampedModel, SoftDeletableModel

User = get_user_model()


class Room(models.Model):
    user1 = models.ForeignKey(User, 
                              on_delete=models.SET_NULL, 
                              null=True, related_name='chats', 
                              db_index=True)
    user2 = models.ForeignKey(User, 
                              on_delete=models.SET_NULL, 
                              null=True, 
                              related_name='recieved_chats', 
                              db_index=True)
    
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

    def __str__(self):
        return _("Chats between ") + f"{self.user1_id}, {self.user2_id}"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.author} {self.room})"

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

# class MessageModel(TimeStampedModel, SoftDeletableModel):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Author"),
#                                related_name='from_user', db_index=True)
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Recipient"),
#                                   related_name='to_user', db_index=True)
#     text = models.TextField(verbose_name=_("Text"), blank=True)
#     file = models.ForeignKey(UploadedFile, related_name='message', on_delete=models.DO_NOTHING,
#                              verbose_name=_("File"), blank=True, null=True)

#     read = models.BooleanField(verbose_name=_("Read"), default=False)
#     all_objects = models.Manager()

#     room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="messages")
#     text = models.TextField(max_length=500)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message({self.user} {self.room})"