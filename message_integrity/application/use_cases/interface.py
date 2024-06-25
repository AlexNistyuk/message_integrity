from abc import ABC, abstractmethod


class IUseCase(ABC):
    @abstractmethod
    def register(self, *args, **kwargs) -> None:
        raise NotImplementedError
