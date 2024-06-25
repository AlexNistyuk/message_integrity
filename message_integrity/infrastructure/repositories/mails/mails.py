from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from infrastructure.repositories.mails.interface import IMaleRepository
from mails.models import Mail


class MaleRepository(IMaleRepository):
    model = Mail

    @sync_to_async
    def get_part(self, user_id: int, slice_obj: slice) -> QuerySet:
        return self.model.objects.filter(receiver_id=user_id)[slice_obj]

    @sync_to_async
    def get_mails_count_by_user_id(self, user_id: int) -> int:
        return self.model.objects.filter(receiver_id=user_id).count()
