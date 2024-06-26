import json
from email import utils
from email.header import decode_header
from email.message import Message
from math import ceil
from typing import Callable

import aioimaplib.aioimaplib
from application.factories.imap import ImapFactory
from application.services.interface import ImapServiceABC
from application.use_cases.mails.interface import IMailUseCase
from application.use_cases.users.interface import IUserUseCase
from infrastructure.repositories.mails.interface import IMaleRepository
from infrastructure.repositories.mails.mails import MaleRepository
from users.models import User

from message_integrity.settings import MAIL_GAP


class MailUseCase(IMailUseCase):
    def __init__(self, user_use_case: IUserUseCase, ws_send: Callable) -> None:
        self.user_use_case = user_use_case
        self.ws_send = ws_send
        self.mail_repository: IMaleRepository = MaleRepository()

    async def check_and_upload_mails(self, user_id: int) -> None:
        receiver = await self.user_use_case.get_by_id(user_id)
        imap_service = ImapFactory.get_service_by_email_type(receiver.email_type)

        try:
            async with imap_service.login(
                receiver.email, receiver.password
            ) as imap_service:
                mails_uids, all_mails_uids_length = await self.__check_mails(
                    receiver, imap_service
                )
                await self.__upload_mails(
                    imap_service, receiver, mails_uids, all_mails_uids_length
                )
        except aioimaplib.aioimaplib.Abort:
            await self.ws_send(
                text_data=json.dumps(
                    {"mode": "error", "reason": "Cannot create connection"}
                )
            )

    async def __check_mails(
        self, receiver: User, imap_service: ImapServiceABC
    ) -> tuple[set, int]:
        mails_uids = await imap_service.get_mails_uids()
        mails_count_from_db = await self.mail_repository.get_mails_count_by_user_id(
            receiver.pk
        )

        all_mails = len(mails_uids)
        read_mails = 0

        if mails_count_from_db == 0:
            await self.__send_checked_mails(all_mails, read_mails)

        for i in range(ceil(mails_count_from_db / MAIL_GAP)):
            slice_obj = slice(i * MAIL_GAP, (i + 1) * MAIL_GAP)
            mails_from_db = await self.mail_repository.get_part(receiver.pk, slice_obj)

            async for mail in mails_from_db:
                if mail.uid in mails_uids:
                    read_mails += 1

                try:
                    mails_uids.remove(mail.uid)
                except KeyError:
                    ...

            await self.__send_checked_mails(all_mails, read_mails)

        return mails_uids, all_mails

    async def __send_checked_mails(self, all_mails: int, read_mails: int) -> None:
        await self.ws_send(
            text_data=json.dumps(
                {"all": all_mails, "checked": read_mails, "mode": "check"}
            )
        )

    async def __upload_mails(
        self,
        imap_service: ImapServiceABC,
        receiver: User,
        upload_mails_uids: set,
        all_mails_uids_length: int,
    ) -> None:
        upload_mails_uids_length = len(upload_mails_uids)
        if upload_mails_uids_length == 0:
            await self.__send_uploaded_mail(
                all_mails_uids_length, all_mails_uids_length
            )

        uploaded_mails = all_mails_uids_length - upload_mails_uids_length
        for uid in upload_mails_uids:
            message = await imap_service.get_mail_by_uid(uid)
            mail_data, mail_files_data = self.__get_data_from_message(
                receiver, uid, message
            )

            uploaded_mail = await self.mail_repository.create(
                mail_data, mail_files_data
            )
            if uploaded_mail is None:
                continue

            uploaded_mails += 1

            mail_data["id"] = uploaded_mail.pk

            await self.__send_uploaded_mail(
                all_mails_uids_length,
                uploaded_mails,
                mail_data,
                list(mail_files_data.keys()),
            )

    async def __send_uploaded_mail(
        self,
        mails_uids_length: int,
        uploaded_mails: int,
        mail_data: dict | None = None,
        mail_files: list | None = None,
    ) -> None:
        if mail_data is not None:
            mail_data["received_date"] = (
                None
                if mail_data["received_date"] is None
                else str(mail_data["received_date"])
            )
            mail_data["sent_date"] = (
                None if mail_data["sent_date"] is None else str(mail_data["sent_date"])
            )
            mail_data.pop("receiver")

        await self.ws_send(
            text_data=json.dumps(
                {
                    "mode": "upload",
                    "all": mails_uids_length,
                    "uploaded": uploaded_mails,
                    "data": {"mail": mail_data, "files": mail_files},
                }
            )
        )

    def __get_data_from_message(
        self, receiver: User, uid: str, message: Message
    ) -> tuple[dict, dict]:
        try:
            sent_date = utils.parsedate_to_datetime(message["Date"])
        except ValueError:
            sent_date = None

        try:
            raw_received_date = message["Received"].split("\n")[-1].strip()
            received_date = utils.parsedate_to_datetime(raw_received_date)
        except (AttributeError, ValueError):
            received_date = None

        subject = self.__get_text(message["Subject"])
        text = self.__get_message_text(message)
        files = self.__get_message_files(message)

        return {
            "subject": subject,
            "sent_date": sent_date,
            "received_date": received_date,
            "uid": uid,
            "receiver": receiver,
            "text": text,
        }, files

    def __get_message_text(self, message: Message) -> str:
        text = ""
        for part in message.walk():
            if (
                part.get_content_maintype() == "text"
                and part.get_content_subtype() == "plain"
            ):
                try:
                    text += part.get_payload(decode=True).decode() + "\n"
                except UnicodeDecodeError:
                    ...

        return text

    def __get_message_files(self, message: Message) -> dict:
        message_files = {}

        for part in message.walk():
            if part.get_content_disposition() == "attachment":
                filename = self.__get_text(part.get_filename())
                message_files[filename] = part.get_payload(decode=True)

        return message_files

    def __get_text(self, text: str) -> str | None:
        try:
            return decode_header(text)[0][0].decode()
        except AttributeError:
            return text
        except (UnicodeDecodeError, TypeError):
            return
