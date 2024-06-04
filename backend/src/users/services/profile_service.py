from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from src.data.handlers import AvatarFileHandler  # unused import
    from src.data.interfaces import (
        IEventHandler,
        IFileHandler,
    )
    from src.users.interfaces import IProfileRepository


class ProfileService:
    def __init__(
        self,
        repository: "IProfileRepository",
        event_handler: "IEventHandler",
        image_handler: "IFileHandler",
        *args,
        **kwargs,
    ):
        self.profile_repository = repository
        self.event = event_handler
        self.avatar = cast("AvatarFileHandler", image_handler)
        super().__init__(*args, **kwargs)

    def create_profile(self):
        self.event.sub(["register_profile_response"])
        while data := self.event.get():
            user_id = data["user_id"]
            profile = data["profile_create"]
            avatar = self.avatar.get_avatar(object_key=user_id)
            self.profile_repository.create_profile(
                user_id=user_id,
                profile_create=profile,
                avatar=avatar,
            )
