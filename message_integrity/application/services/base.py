from typing import Self

from aioimaplib import IMAP4_SSL, aioimaplib
from application.services.interface import ImapServiceABC


class ImapServiceBase(ImapServiceABC):
    host: str
    email: str
    password: str
    initial_folder: str
    imap_client: IMAP4_SSL

    def login(self, email: str, password: str, initial_folder: str = "INBOX") -> Self:
        self.email = email
        self.password = password
        self.initial_folder = initial_folder

        return self

    async def __aenter__(
        self,
    ) -> Self:
        # TODO catch error while creating connection!

        self.imap_client = aioimaplib.IMAP4_SSL(host=self.host)
        await self.imap_client.wait_hello_from_server()
        await self.imap_client.login(self.email, self.password)
        await self.imap_client.select(self.initial_folder)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.imap_client.logout()

    async def get_mails_uids(self) -> set[str]:
        response = await self.imap_client.fetch("1:*", "UID")

        uids = set()
        for item in response.lines[:-1]:
            uid = item.decode().split()[-1].replace(")", "")

            uids.add(uid)

        return uids
