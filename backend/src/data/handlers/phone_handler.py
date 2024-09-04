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
from src.users.schemas import PhoneNumberSchema

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
            if response["messages"][0]["message_id"]:
                logger.info(
                    """
                    Send sms with title: [blue]%s[/], 
                    message: [blue]%s[/] 
                    to number: [blue]%s[/]
                    """,
                    title,
                    message,
                    number,
                    extra={"markup": True},
                )
                return True
        else:
            logger.error(
                "Sms not sent with error: [red]%s[/]",
                response["messages"][0]["error_text"],
                extra={"markup": True},
            )
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
        if response["status"] == "0":
            request_id = response["request_id"]
            if request_id:
                logger.info(
                    "Created verify token : [blue]%s[/] for number: [blue]%s[/]",
                    request_id,
                    number,
                    extra={"markup": True},
                )
                self.cache.set_value(
                    key=request_id,
                    value=number,
                    expire=timedelta(minutes=5),
                )
                return request_id
        else:
            logger.error(
                "Verify number error: [red]%s[/]",
                response["error_text"],
                extra={"markup": True},
            )
            return None

    def verify_number_code(
        self,
        request_id: str,
        code: str,
        **kwargs,
    ) -> bool:
        response = self.verify.check(
            request_id=request_id,
            code=code,
        )
        if response["status"] == "0":
            number = self.cache.get_value(key=request_id)
            event_id = response["event_id"]
            if number and event_id:
                logger.info(
                    "Number code verified: [blue]%s[/] for number: [blue]%s[/] with event_id: [blue]%s[/]",
                    code,
                    number,
                    event_id,
                    extra={"markup": True},
                )
                return True
        else:
            logger.error(
                "Verify number code error: [red]%s[/]",
                response["error_text"],
                extra={"markup": True},
            )
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

    def _get_sms(self, number: str) -> Optional[dict]:
        sms_data = self.cache.get_value(key=f"fake_sms_{number}")
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
        self.cache.set_value(
            key=f"fake_sms_{number}",
            value=data,
            expire=timedelta(minutes=5),
        )
        sms_data = self._get_sms(number=number)
        if sms_data:
            logger.info(
                """
                Send sms with title: [blue]%s[/], 
                message: [blue]%s[/] 
                to number: [blue]%s[/]
                """,
                title,
                message,
                number,
                extra={"markup": True},
            )
            return True
        logger.info(
            "Sms not sent to number [blue]%s[/]",
            number,
            extra={"markup": True},
        )
        return False

    def verify_number(
        self,
        number: str,
        brand: str = "Olivin Store",
        **kwargs,
    ) -> Optional[str]:
        request_id = create_jwt_token(
            data={
                "number": number,
            },
            expires_delta=timedelta(minutes=5),
        )
        logger.info(
            "Created verify token : [blue]%s[/] for number: [blue]%s[/]",
            request_id,
            number,
            extra={"markup": True},
        )
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
        if number:
            logger.info(
                "Number code verified: [blue]%s[/] for number: [blue]%s[/]",
                code,
                number,
                extra={"markup": True},
            )
            return True
        logger.error(
            "Verify number code error: [red]%s[/]",
            "Invalid verification code",
            extra={"markup": True},
        )
        return False
