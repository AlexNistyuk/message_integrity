from abc import ABC, abstractmethod

from django.db import models
from django.db.models import QuerySet


class IMaleRepository(ABC):
    model: models.Model

    @abstractmethod
    def get_part(self, *args, **kwargs) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_mails_count_by_user_id(self, *args, **kwargs) -> int:
        raise NotImplementedError
