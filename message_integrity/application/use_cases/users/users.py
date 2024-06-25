from application.use_cases.users.interface import IUserUseCase
from infrastructure.repositories.users.users import IUserRepository, UserRepository
from users.models import User


class UserUseCase(IUserUseCase):
    def __init__(self):
        self.repository: IUserRepository = UserRepository()

    def register(self, data: dict) -> User:
        email = data.get("email")
        password = data.get("password")
        email_type = data.get("email_type").value

        return self.repository.register(email, password, email_type)

    async def get_by_id(self, user_id: int) -> User:
        return await self.repository.get_by_id(user_id)
