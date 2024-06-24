from message_integrity.application.services.base import ImapServiceBase


class YandexImapService(ImapServiceBase):
    host: str = "imap.yandex.com"
