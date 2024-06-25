import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from presentation.websocket.routers import urlpatterns as websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "message_integrity.settings")


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
