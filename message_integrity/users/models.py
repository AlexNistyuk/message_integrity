from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from domain.enums.emails import EmailType

email_type_choices = [(choice, choice.value) for choice in EmailType]


class User(AbstractBaseUser):
    email = models.EmailField(max_length=319, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    email_type = models.CharField(max_length=6, choices=email_type_choices, null=False)
    last_login = None

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "email_type"]
