from message_integrity.application.services.base import ImapServiceBase


class GmailImapService(ImapServiceBase):
    host: str = "imap.gmail.com"
