# import logging
# from typing import Optional
# from uuid import UUID
#
# from django.http import HttpRequest, JsonResponse
# from ninja import UploadedFile
# from ninja.constants import NOT_SET
# from ninja_extra import api_controller, route
# from ninja_extra.exceptions import APIException
# from ninja_extra.permissions.common import IsAuthenticated
#
# from src.common.schemas import MessageSchema
# from src.core.interceptors import AuthBearer
# from src.core.storage import get_storage
# from src.data.handlers import AvatarFileHandler, EventHandler
# from src.data.managers import EventManager
# from src.users.errors import UserNotFound
# from src.users.repositories import UserRepository
# from src.users.schemas import (
#     EmailUpdateErrorSchema,
#     EmailUpdateSchema,
#     EmailUpdateSuccessSchema,
#     ProfileUpdateSchema,
#     UserGetSuccess,
#     UserProfileErrorSchema,
#     UserProfileSuccessSchema,
#     UserProfileUpdateSchema,
#     UserUpdateSchema,
# )
# from src.users.services import UserService
#
# logger = logging.getLogger(__name__)
#
#
# @api_controller(
#     prefix_or_class="/users",
#     auth=NOT_SET,
#     permissions=[],
#     tags=["users"],
# )
# class UserController:
#     repository = UserRepository()
#     avatar_handler = AvatarFileHandler(storage=get_storage())
#     event_handler = EventHandler(manager=EventManager())
#     service = UserService(
#         repository=repository,
#         avatar_handler=avatar_handler,
#         event_handler=event_handler,
#     )
#
#     @route.get(
#         "/{username}",
#     )
#     def get_user(
#         self,
#         username: str,
#     ):
#         return self.service.get_user(username=username)
#
#     @route.post(
#         "/update/email",
#         auth=AuthBearer(),
#         permissions=[IsAuthenticated],
#         response={
#             200: EmailUpdateSuccessSchema,
#             400: EmailUpdateErrorSchema,
#         },
#     )
#     def change_email(
#         self,
#         request: HttpRequest,
#         email_update: EmailUpdateSchema,
#     ):
#         return self.service.change_email(
#             email_update=email_update,
#             user_id=request.user.pk,
#         )
#
#     @route.post(
#         "/update",
#         auth=AuthBearer(),
#         permissions=[IsAuthenticated],
#         response={
#             200: UserProfileSuccessSchema,
#             400: UserProfileErrorSchema,
#         },
#     )
#     def update_user(
#         self,
#         request: HttpRequest,
#         user_update: UserProfileUpdateSchema,
#     ):
#         self.service.update_user(
#             profile_update=ProfileUpdateSchema(
#                 **user_update.model_dump(include={"birth_date"})
#             ),
#             user_update=UserUpdateSchema(
#                 **user_update.model_dump(
#                     include={"first_name", "last_name", "username"}
#                 )
#             ),
#             user_id=request.user.pk,
#         )
#         response = self.service.event.subscribe(
#             event_name="profile_updated", with_receive=False
#         )
#         is_updated = response.get("is_updated")
#
#         if is_updated:
#             return MessageSchema(message="User updated successfully")
#         return MessageSchema(message="User was not updated")
