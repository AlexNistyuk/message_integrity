from application.use_cases.interface import IUseCase
from infrastructure.repositories.interface import IRepository
from infrastructure.repositories.users import UserRepository
from users.models import User


class UserUseCase(IUseCase):
    def __init__(self):
        self.repository: IRepository = UserRepository()

    def register(self, data: dict) -> User:
        email = data.get("email")
        password = data.get("password")
        email_type = data.get("email_type").value

        return self.repository.register(email, password, email_type)
