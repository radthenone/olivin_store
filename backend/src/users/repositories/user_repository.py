from uuid import UUID

from src.users.interfaces import IUserRepository
from src.users.models import User
from src.users.schemas import UserUpdateSchema


class UserRepository(IUserRepository):
    def get_user_by_id(self, user_id: UUID) -> User:
        return User.objects.get(id=user_id)

    def get_user_by_email(self, email: str) -> User:
        return User.objects.get(email=email)

    def get_user_by_username(self, username: str) -> User:
        return User.objects.get(username=username)

    def create_user(self, user: User) -> bool:
        # TODO make later
        pass

    def update_user(self, user: User, user_update: UserUpdateSchema) -> User:
        # TODO make later
        pass

    def delete_user(self, user: User) -> bool:
        # TODO make later
        pass
