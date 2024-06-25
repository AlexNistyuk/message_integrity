from asgiref.sync import sync_to_async
from infrastructure.repositories.users.interface import IUserRepository
from users.models import User


class UserRepository(IUserRepository):
    model = User

    def register(self, email: str, password: str, email_type: str) -> model:
        return self.model.objects.create(
            email=email, password=password, email_type=email_type
        )

    @sync_to_async
    def get_by_id(self, user_id: int) -> model:
        return self.model.objects.get(pk=user_id)
