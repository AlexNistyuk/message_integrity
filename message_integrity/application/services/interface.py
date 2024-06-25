from abc import ABC, abstractmethod
from typing import Self


class ImapServiceABC(ABC):
    @abstractmethod
    def login(self, *args, **kwargs) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_mails_uids(self, *args, **kwargs) -> set[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_mail_by_uid(self, *args, **kwargs):
        raise NotImplementedError
