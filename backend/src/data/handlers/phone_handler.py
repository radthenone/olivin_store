import json
import logging
import random
from datetime import timedelta
from typing import TYPE_CHECKING, Optional
from uuid import UUID

import vonage
from ninja_extra.exceptions import APIException

from src.auth.utils import create_jwt_token, decode_jwt_token
from src.data.clients import VonageClient
from src.data.handlers.redis_handler import CacheHandler
from src.data.interfaces import ICacheHandler, IClient, IPhoneHandler
from src.data.storages import RedisStorage
from src.users.schemas import RegisterPhoneSchema

if TYPE_CHECKING:
    from src.users.interfaces import IProfileRepository

logger = logging.getLogger(__name__)


class VonagePhoneHandler(IPhoneHandler):
    def __init__(
        self,
        client: Optional["IClient"] = None,
        cache: Optional["ICacheHandler"] = None,
        repository: Optional["IProfileRepository"] = None,
    ) -> None:
        self.client = client.connect()
        self.verify = vonage.Verify(client=self.client)
        self.sms = vonage.Sms(client=self.client)
        self.cache = cache
        self.repository = repository

    def send_sms(
        self,
        number: str,
        message: str,
        title: str = "Olivin Store",
        **kwargs,
    ) -> bool:
        response = self.sms.send_message(
            {
                "from": title,
                "to": number,
                "text": message,
            }
        )
        if response["messages"][0]["status"] == "0":
            logger.info("send_sms: %s", response["messages"][0]["message_id"])
            return True
        else:
            logger.info("send_sms: %s", response["messages"][0]["error_text"])
            return False

    def verify_number(
        self,
        number: str,
        brand: str = "Olivin Store",
        **kwargs,
    ) -> Optional[str]:
        response = self.verify.start_verification(
            number=number,
            brand=brand,
        )
        expires = timedelta(minutes=5)
        if response["status"] == "0":
            logger.info("verify_number: %s", response["request_id"])
            request_id = response["request_id"]
            if request_id:
                self.cache.set_value(
                    key=request_id,
                    value=number,
                    expire=expires,
                )
            return response["request_id"]
        else:
            logger.info("verify_number: %s", response["error_text"])
            return None

    def verify_number_code(
        self,
        request_id: str,
        code: str,
        **kwargs,
    ) -> bool:
        if request_id and code:
            response = self.verify.check(
                request_id=request_id,
                code=code,
            )
            if response["status"] == "0":
                number = self.cache.get_value(key=request_id)
                user_id = kwargs.get("user_id")
                if number and user_id:
                    phone = RegisterPhoneSchema(number=number)
                    self.repository.create_profile_phone(phone=phone, user_id=user_id)
                logger.info("verify_number_code: %s", response["request_id"])
                return True
            else:
                logger.info("verify_number_code: %s", response["error_text"])
                return False
        return False


class FakePhoneHandler(IPhoneHandler):
    def __init__(
        self,
        client: Optional["IClient"] = None,
        cache: Optional["ICacheHandler"] = None,
        repository: Optional["IProfileRepository"] = None,
    ) -> None:
        self.cache = cache
        self.repository = repository
        self.client = client

    def _get_sms(self, number: str, user_id: Optional[UUID]) -> Optional[dict]:
        sms_data = self.cache.get_value(key=f"{str(user_id)}_{number}")
        logger.info("get_sms: %s", sms_data)
        if sms_data:
            return sms_data
        return None

    def send_sms(
        self,
        number: str,
        message: str,
        title: str = "Olivin Store",
        **kwargs,
    ) -> bool:
        data = {
            "from": title,
            "to": number,
            "text": message,
        }
        user_id = kwargs.get("user_id")
        self.cache.set_value(
            key=f"{str(user_id)}_{number}",
            value=data,
            expire=timedelta(minutes=5),
        )
        if self._get_sms(number=number, user_id=user_id):
            logger.info("send_sms: %s", number)
            return True
        logger.info("not send_sms: %s", number)
        return False

    def verify_number(
        self,
        number: str,
        brand: str = "Olivin Store",
        **kwargs,
    ) -> Optional[str]:
        expires = timedelta(minutes=5)
        request_id = create_jwt_token(
            data={
                "number": number,
            },
            expires_delta=expires,
        )
        logger.info("verify_number: %s", request_id)
        return request_id

    def verify_number_code(
        self,
        request_id: str,
        code: str,
        **kwargs,
    ) -> bool:
        data = self.cache.get_value(key=request_id)
        if not data["code"] == code:
            raise APIException("Invalid verification code", code=400)
        token_decoded = decode_jwt_token(token=request_id)
        number = token_decoded["number"]
        user_id = kwargs.get("user_id")
        if number and user_id:
            phone = RegisterPhoneSchema(number=number)
            self.repository.create_profile_phone(phone=phone, user_id=user_id)
            return True
        return False
