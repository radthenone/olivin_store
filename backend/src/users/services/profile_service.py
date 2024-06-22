from typing import TYPE_CHECKING, cast

from src.users.schemas import ProfileCreateSchema

if TYPE_CHECKING:
    from src.data.handlers import AvatarFileHandler  # unused import
    from src.data.interfaces import (
        ICacheHandler,
        IEventHandler,
        IFileHandler,
    )
    from src.users.interfaces import IProfileRepository, IUserRepository


class ProfileService:
    def __init__(
        self,
        profile_repository: "IProfileRepository",
        user_repository: "IUserRepository",
        event_handler: "IEventHandler",
        avatar_handler: "IFileHandler",
        cache_handler: "ICacheHandler",
        *args,
        **kwargs,
    ):
        self.profile_repository = profile_repository
        self.user_repository = user_repository
        self.event = event_handler
        self.avatar = cast("AvatarFileHandler", avatar_handler)
        self.cache = cache_handler
        super().__init__(*args, **kwargs)

    def handle_user_created(self):
        while True:
            event_data = self.event.subscribe("user_created")
            if event_data:
                if event_data["user_id"] and event_data["profile_create"]:
                    user_id = event_data["user_id"]
                    profile = event_data["profile_create"]
                    avatar = self.avatar.get_avatar(object_key=user_id)
                    user = self.user_repository.get_user_by_id(user_id=user_id)

                    if "?" in avatar:
                        avatar = avatar.rsplit("?")[0]

                    if self.profile_repository.create_profile(
                        profile_create=ProfileCreateSchema(**profile),
                        avatar=avatar,
                        user=user,
                    ):
                        is_created = True
                    else:
                        is_created = False

                    self.event.publish(
                        "profile_created",
                        {"user_id": user_id, "is_created": is_created},
                    )
