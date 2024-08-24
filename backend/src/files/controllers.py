from django.http import HttpRequest
from ninja import UploadedFile
from ninja_extra import api_controller, permissions, route

from src.common.responses import ORJSONResponse
from src.core.interceptors import AuthBearer
from src.core.storage import get_storage
from src.data.handlers import (
    AvatarFileHandler,
)
from src.files.services import FileService


@api_controller(
    prefix_or_class="/files",
    auth=AuthBearer(),
    permissions=[permissions.IsAuthenticated],
    tags=["files"],
)
class FileController:
    avatar_handler = AvatarFileHandler(storage=get_storage())

    service = FileService(
        avatar_handler,
    )

    @route.get("/avatar/get")
    def get_avatar(self, request: HttpRequest):
        return ORJSONResponse(
            self.service.get_avatar(
                request.user.pk,
            ).model_dump(),
            status=200,
        )

    @route.post("/avatar/upload")
    def upload_avatar(
        self,
        file: UploadedFile,
        request: HttpRequest,
    ):
        return ORJSONResponse(
            data=self.service.upload_avatar(
                file=file,
                user_id=request.user.pk,
            ).model_dump(),
            status=201,
        )

    @route.post("/avatar/update")
    def update_avatar(
        self,
        file: UploadedFile,
        request: HttpRequest,
    ):
        return ORJSONResponse(
            data=self.service.update_avatar(
                file=file,
                user_id=request.user.pk,
            ).model_dump(),
            status=200,
        )

    @route.delete("/avatar/delete")
    def delete_avatar(self, request: HttpRequest):
        return ORJSONResponse(
            data=self.service.delete_avatar(
                user_id=request.user.pk,
            ).model_dump(),
            status=200,
        )
