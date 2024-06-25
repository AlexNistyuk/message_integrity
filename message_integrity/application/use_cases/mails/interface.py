from abc import ABC, abstractmethod


class IMailUseCase(ABC):
    @abstractmethod
    def check_and_upload_mails(self, *args, **kwargs) -> None:
        raise NotImplementedError
