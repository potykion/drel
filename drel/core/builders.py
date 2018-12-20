from typing import Any, Optional

from .models import FullRequestLog, RequestLog, ResponseLog, DEFAULT_LOG_TYPE


class BaseFullRequestLogBuilder:
    def __init__(self, type_: Optional[str] = None):
        self.type = type_ or DEFAULT_LOG_TYPE

    def __call__(self, request: Any, response: Any) -> FullRequestLog:
        return FullRequestLog(
            request=self.request_to_log(request),
            response=self.response_to_log(response),
            type=self.type,
        )

    def request_to_log(self, request: Any) -> RequestLog:
        raise NotImplementedError()

    def response_to_log(self, response: Any) -> ResponseLog:
        raise NotImplementedError()
