import json
from math import ceil
from typing import Callable

from application.factories.imap import ImapFactory
from application.use_cases.users.interface import IUserUseCase
from infrastructure.repositories.mails.interface import IMaleRepository
from infrastructure.repositories.mails.mails import MaleRepository


class MailUseCase:
    def __init__(self, user_use_case: IUserUseCase, ws_send: Callable) -> None:
        self.user_use_case = user_use_case
        self.ws_send = ws_send
        self.mail_repository: IMaleRepository = MaleRepository()
        self.mail_gap = 2

    async def check_added_mails(self, user_id: int):
        user = await self.user_use_case.get_by_id(user_id)
        imap_service = ImapFactory.get_service_by_email_type(user.email_type)

        async with imap_service.login(user.email, user.password) as imap_service:
            mails_uids = await imap_service.get_mails_uids()
            mails_count_from_db = await self.mail_repository.get_mails_count_by_user_id(
                user_id
            )

        all_mails = len(mails_uids)
        read_mails = 0

        for i in range(ceil(mails_count_from_db / self.mail_gap)):
            slice_obj = slice(i * self.mail_gap, (i + 1) * self.mail_gap)
            mails_from_db = await self.mail_repository.get_part(user_id, slice_obj)

            async for mail in mails_from_db:
                if mail.uid in mails_uids:
                    read_mails += 1

                mails_uids.remove(mail.uid)

            await self.ws_send(
                text_data=json.dumps(
                    {"all": all_mails, "checked": read_mails, "mode": "check"}
                )
            )

        return mails_count_from_db
