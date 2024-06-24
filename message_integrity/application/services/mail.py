from message_integrity.application.services.base import ImapServiceBase


class MailImapService(ImapServiceBase):
    host: str = "imap.mail.ru"
