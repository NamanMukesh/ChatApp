import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from Chat.middleware import TokenAuthMiddleware
import Chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            Chat.routing.websocket_urlpatterns
        )
    ),
})