from abc import ABC, abstractmethod

from message_integrity.application.services.interface import ImapServiceABC
from message_integrity.domain.enums.emails import EmailType


class ImapFactoryABC(ABC):
    @abstractmethod
    def get_service_by_email_type(self, email_type: EmailType) -> ImapServiceABC | None:
        raise NotImplementedError
