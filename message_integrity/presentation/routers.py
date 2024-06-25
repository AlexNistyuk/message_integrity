from django.urls import include, path

from .api.routers import urlpatterns as api_routers

urlpatterns = [
    path("api/", include(api_routers)),
]
