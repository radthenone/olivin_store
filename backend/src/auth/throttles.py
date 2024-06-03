import json
import logging
from typing import Optional

from ninja_extra.throttling import AnonRateThrottle

logger = logging.getLogger(__name__)


class RegisterMailThrottle(AnonRateThrottle):
    rate = "10/min"
    scope = "minutes"

    def __init__(self):
        super().__init__()
        self.timed = self.calculate_expiration_time()

    def allow_request(self, request):
        allowed = super().allow_request(request)
        email = json.loads(request.body)["email"]
        key = self.cache.get(email)
        self.now = self.timer()
        if key:
            logger.info("Email %s already registered", json.loads(key)["email"])
            allowed = False
        else:
            self.cache.set(
                key=email,
                value=json.dumps({"email": email}),
                timeout=self.timed,
            )
            self.history.insert(0, self.now)
        return allowed

    def calculate_expiration_time(self):
        rate_value, rate_unit = self.rate.split("/")
        rate_value = int(rate_value)

        if rate_unit == "min":
            expiration_time = rate_value * 60
        elif rate_unit == "hour":
            expiration_time = rate_value * 3600
        else:
            expiration_time = rate_value
        return expiration_time

    def wait(self) -> Optional[float]:
        if self.history:
            remaining_duration = self.timed - (self.now - self.history[-1])
        else:
            remaining_duration = self.timed

        if remaining_duration > 0:
            return remaining_duration
        return None


class RegisterThrottle(AnonRateThrottle):
    rate = "2/min"
    scope = "minutes"
