from application.use_cases.users import UserUseCase
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from users.models import User
from users.serializers import UserRegisterSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_action_classes = {
        "create": UserRegisterSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserUseCase().register(serializer.validated_data)

        data = self.get_serializer(user).data
        data["email_type"] = data["email_type"].value

        return Response(data, status=status.HTTP_201_CREATED)
