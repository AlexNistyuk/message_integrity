from application.services.base import ImapServiceBase


class YandexImapService(ImapServiceBase):
    host: str = "imap.yandex.com"
