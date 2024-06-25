from abc import ABC, abstractmethod


class IUserUseCase(ABC):
    @abstractmethod
    def register(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        raise NotImplementedError
