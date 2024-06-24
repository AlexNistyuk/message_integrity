from abc import ABC, abstractmethod
from typing import Self


class ImapServiceABC(ABC):
    @abstractmethod
    def login(self, *args, **kwargs) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    # TODO add type hint for method below
    @abstractmethod
    def get_new_mails(self, *args, **kwargs):
        raise NotImplementedError
