from django.contrib import admin

from .models import Room
from .models import Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'user1', 'user2', 'start_time',)
    

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'room', 'author', 'text', 'attachment', 'timestamp',)