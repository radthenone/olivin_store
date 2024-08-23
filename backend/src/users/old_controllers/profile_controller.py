# import logging
#
# from django.http import HttpRequest, JsonResponse
# from ninja.constants import NOT_SET
# from ninja_extra import api_controller, route
# from ninja_extra.permissions.common import IsAuthenticated
#
# from src.core.handler import get_phone_handler
# from src.core.interceptors import AuthBearer
# from src.core.storage import get_storage
# from src.data.handlers import AvatarFileHandler, CacheHandler, EventHandler
# from src.data.managers import EventManager
# from src.data.storages import RedisStorage
# from src.users.repositories import ProfileRepository
# from src.users.schemas import CreatePhoneSchema, RegisterPhoneSchema
# from src.users.services import ProfileService
#
# logger = logging.getLogger(__name__)
#
#
# @api_controller(
#     prefix_or_class="/profiles",
#     auth=AuthBearer(),
#     permissions=[],
#     tags=["profiles"],
# )
# class ProfileController:
#     profile_repository = ProfileRepository()
#     event_handler = EventHandler(manager=EventManager())
#     avatar_handler = AvatarFileHandler(storage=get_storage())
#     cache_handler = CacheHandler(pool_storage=RedisStorage())
#
#     service = ProfileService(
#         repository=profile_repository,
#         event_handler=event_handler,
#         avatar_handler=avatar_handler,
#         cache_handler=cache_handler,
#         phone_handler=get_phone_handler(
#             cache=cache_handler,
#             repository=profile_repository,
#         ),
#     )
#
#     @route.post(
#         "/phone/register",
#         auth=AuthBearer(),
#         permissions=[IsAuthenticated],
#     )
#     def register_phone(
#         self,
#         phone: RegisterPhoneSchema,
#         request: HttpRequest,
#     ):
#         return self.service.register_phone(
#             user_id=request.user.pk,
#             phone=phone,
#         )
#
#     @route.post(
#         "/phone/create",
#         auth=AuthBearer(),
#         permissions=[IsAuthenticated],
#     )
#     def create_phone(
#         self,
#         phone: CreatePhoneSchema,
#         request: HttpRequest,
#     ):
#         return self.service.create_phone(
#             user_id=request.user.pk,
#             phone=phone,
#         )
