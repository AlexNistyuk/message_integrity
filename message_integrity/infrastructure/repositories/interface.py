from abc import ABC, abstractmethod

from django.db import models


class IRepository(ABC):
    model: models.Model

    @abstractmethod
    def register(self, *args, **kwargs):
        raise NotImplementedError
