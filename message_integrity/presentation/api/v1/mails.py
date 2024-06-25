from django.urls import path
from mails.views import MailAPIView

urlpatterns = [path("mails/<int:pk>", MailAPIView.as_view(), name="mails")]
