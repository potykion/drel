from typing import Any, Optional, Dict

from drel.core import config
from .models import FullRequestLog, RequestLog, ResponseLog


class BaseFullRequestLogBuilder:
    def __init__(self, type: Optional[str] = None, user: Any = None):
        self.type = type or config.DEFAULT_LOG_TYPE
        self.user = user

    def __call__(self, request: Any, response: Any) -> FullRequestLog:
        return FullRequestLog(
            request=self.request_to_log(request),
            response=self.response_to_log(response),
            type=self.type,
            user=self._serialize_user(),
        )

    def _serialize_user(self) -> Dict:
        user_data, _ = config.USER_SERIALIZER.dump(self.user)
        return user_data

    def request_to_log(self, request: Any) -> RequestLog:
        raise NotImplementedError()

    def response_to_log(self, response: Any) -> ResponseLog:
        raise NotImplementedError()
