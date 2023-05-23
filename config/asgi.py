import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator  # new
from django.core.asgi import get_asgi_application
from apps.chats import routing  # new
from .tokenauth_middleware import TokenAuthMiddleware  # new



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(  # new
        TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)))
})