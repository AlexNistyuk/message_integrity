from django.urls import path
from mails.views import MailWebsocket

urlpatterns = [
    path("ws/<int:pk>", MailWebsocket.as_asgi()),
]
