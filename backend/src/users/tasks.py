import logging
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.core.celery import celery
from src.users.repositories import ProfileRepository, UserRepository
from src.users.schemas import ProfileCreateSchema, UserCreateSchema

if TYPE_CHECKING:
    from src.users.types import UserType

logger = logging.getLogger(__name__)


@celery.task(queue="tasks")
def create_user_task(user_create: dict) -> Optional[str]:
    logger.info("Received user creation request: %s", user_create)
    repository = UserRepository()

    try:
        user = repository.create_user(
            user_create_schema=UserCreateSchema(**user_create)
        )
        if user:
            logger.info("create_user_task: %s", user.to_dict(include=["id", "email"]))
            logger.info(
                "User created successfully with email [blue]%s[/]",
                user.email,
                extra={"markup": True},
            )
            return str(user.id)
        else:
            logger.warning("User creation failed, repository returned None.")
    except Exception as e:
        logger.error("An exception occurred: %s", str(e))

    logger.info(
        "User creation failed for email [blue]%s[/]",
        user_create["email"],
        extra={"markup": True},
    )
    return None


@celery.task(queue="tasks")
def delete_user_task(user_id: str) -> bool:
    repository = UserRepository()
    return repository.delete_user(user_id=UUID(user_id))


@celery.task(queue="tasks")
def delete_profile_task(user_id: str) -> bool:
    repository = ProfileRepository()
    return repository.delete_profile(user_id=UUID(user_id))


@celery.task(queue="tasks")
def create_profile_task(profile_create_data: dict, user_id: str) -> Optional[str]:
    repository = ProfileRepository()
    profile = repository.create_profile(
        profile_create=ProfileCreateSchema(**profile_create_data),
        user_id=UUID(user_id),
    )
    if profile:
        logger.info(
            "create_profile_task: %s", profile.to_dict(include=["id", "birth_date"])
        )
        logger.info(
            "Profile created successfully for user [blue]%s[/]",
            user_id,
            extra={"markup": True},
        )
        return str(profile.id)
    logger.info(
        "Profile creation failed for user [blue]%s[/]",
        user_id,
        extra={"markup": True},
    )
    return None
