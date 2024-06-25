from django.urls import include, path

from .v1.mails import urlpatterns as v1_mails
from .v1.users import urlpatterns as v1_users

urlpatterns = [
    path("v1/", include(v1_users + v1_mails)),
]
