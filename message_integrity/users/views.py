from application.use_cases.users.users import UserUseCase
from django.shortcuts import redirect, render
from django.urls import reverse
from domain.enums.emails import EmailType
from rest_framework import mixins, viewsets
from users.models import User
from users.serializers import UserRegisterSerializer


def home_page(request):
    email_type_choices = [choice.value for choice in EmailType]

    return render(request, "hello.html", {"choices": email_type_choices})


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

        url_redirect = reverse("mails", args=(user.pk,))

        return redirect(url_redirect, permanent=True)
