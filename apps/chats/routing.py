from django.urls import re_path, path
from djangochannelsrestframework.consumers import view_as_consumer

from . import consumers
from .views import RoomViewSet

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    path("ws/room/", view_as_consumer(RoomViewSet.as_view({'get': 'list'},)))
]