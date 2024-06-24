from typing import Self

from imap_tools import MailBox

from message_integrity.application.services.interface import ImapServiceABC


class ImapServiceBase(ImapServiceABC):
    host: str
    username: str
    password: str
    initial_folder: str

    def login(
        self, username: str, password: str, initial_folder: str = "INBOX"
    ) -> Self:
        self.username = username
        self.password = password
        self.initial_folder = initial_folder

        return self

    def __enter__(
        self,
    ) -> Self:
        # TODO catch error while creating connection!
        self.__mailbox = (
            MailBox(self.host)
            .login(self.username, self.password, self.initial_folder)
            .__enter__()
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__mailbox.__exit__(exc_type, exc_val, exc_tb)

    def get_new_mails(self, handled_mails_count: int):
        slice_obj = slice(handled_mails_count, stop=None)

        self.__mailbox.fetch(limit=slice_obj)
