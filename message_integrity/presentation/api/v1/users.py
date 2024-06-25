from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

user_router = DefaultRouter()
user_router.register(r"users", UserViewSet)

urlpatterns = user_router.urls
