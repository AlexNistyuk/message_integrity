from application.factories.interface import ImapFactoryABC
from application.services.gmail import GmailImapService
from application.services.interface import ImapServiceABC
from application.services.mail import MailImapService
from application.services.yandex import YandexImapService
from domain.enums.emails import EmailType


class ImapFactory(ImapFactoryABC):
    __service_map = {
        EmailType.GMAIL.value: GmailImapService(),
        EmailType.YANDEX.value: YandexImapService(),
        EmailType.MAIL.value: MailImapService(),
    }

    def get_service_by_email_type(self, email_type: EmailType) -> ImapServiceABC | None:
        return self.__service_map.get(email_type.value)
