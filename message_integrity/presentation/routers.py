from django.urls import include, path
from users.views import home_page

from .api.routers import urlpatterns as api_routers

urlpatterns = [path("api/", include(api_routers)), path("", home_page, name="home")]
