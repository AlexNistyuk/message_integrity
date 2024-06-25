from application.services.base import ImapServiceBase


class MailImapService(ImapServiceBase):
    host: str = "imap.mail.ru"
