from django.urls import include, path

from .v1.users import urlpatterns as v1_users

urlpatterns = [
    path("v1/", include(v1_users)),
]
