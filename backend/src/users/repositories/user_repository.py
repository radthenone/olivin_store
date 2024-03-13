import logging
from uuid import UUID

from src.users.interfaces import IUserRepository
from src.users.models import User
from src.users.schemas import SuperUserCreateSchema, UserCreateSchema, UserUpdateSchema

logger = logging.getLogger(__name__)


class UserRepository(IUserRepository):
    def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        return User.objects.get(id=user_id)

    def get_user_by_email(
        self,
        email: str,
    ) -> User:
        return User.objects.get(email=email)

    def get_user_by_username(
        self,
        username: str,
    ) -> User:
        return User.objects.get(username=username)

    def create_user(
        self,
        user_obj: User,
        user_create: UserCreateSchema,
    ) -> bool:
        try:
            user_db = User(
                email=user_create.email,
                password=user_create.password,
                username=user_create.username,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
            )

            setattr(user_db, "is_staff", False)
            setattr(user_db, "is_superuser", False)

            user_db.set_password(user_create.password)
            user_db.save()
            logger.info("User created successfully with email %s", user_create.email)
        except Exception as error:
            logger.error("Error while creating user %s", error)
            return False
        return True

    def create_superuser(
        self,
        user_obj: User,
        user_super_create: SuperUserCreateSchema,
    ) -> bool:
        try:
            user_db = User(
                email=user_super_create.email,
                password=user_super_create.password,
                is_staff=user_super_create.is_staff,
                is_superuser=user_super_create.is_superuser,
            )
            user_db.set_password(user_super_create.password)
            user_db.save()
            logger.info(
                "Superuser created successfully with email %s", user_super_create.email
            )
        except Exception as error:
            logger.error("Error while creating superuser %s", error)
            return False
        return True

    def update_user(
        self,
        user_obj: User,
        user_update: UserUpdateSchema,
    ) -> User:
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user_obj, field, value)
        user_obj.save()
        return user_obj

    def delete_user(
        self,
        user_id: UUID,
    ) -> bool:
        # TODO make later
        pass
