from abc import ABC, abstractmethod

from django.db import models


class IUserRepository(ABC):
    model: models.Model

    @abstractmethod
    def register(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, *args, **kwargs):
        raise NotImplementedError
