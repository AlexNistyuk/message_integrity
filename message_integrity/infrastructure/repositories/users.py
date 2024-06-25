from infrastructure.repositories.interface import IRepository
from users.models import User


class UserRepository(IRepository):
    model = User

    def register(self, email: str, password: str, email_type: str) -> model:
        return self.model.objects.create(
            email=email, password=password, email_type=email_type
        )
