import django.db.transaction
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from infrastructure.repositories.mails.interface import IMaleRepository
from mails.models import Mail, MailFiles


class MaleRepository(IMaleRepository):
    model = Mail
    mail_files_model = MailFiles

    @sync_to_async
    def get_part(self, user_id: int, slice_obj: slice) -> QuerySet:
        return self.model.objects.filter(receiver_id=user_id)[slice_obj]

    @sync_to_async
    def get_mails_count_by_user_id(self, user_id: int) -> int:
        return self.model.objects.filter(receiver_id=user_id).count()

    @sync_to_async
    def create(self, mail_data: dict, mail_files_data: dict) -> Mail | None:
        mail = self.model.objects.create(**mail_data)

        for filename, content in mail_files_data.items():
            content_file = ContentFile(content, name=filename)

            try:
                self.mail_files_model.objects.create(mail=mail, file=content_file)
            except (OSError, django.core.exceptions.SuspiciousFileOperation):
                continue
        return mail
