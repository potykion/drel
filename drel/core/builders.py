from typing import Any
from typing import Optional

from drel.core.models import FullRequestLog
from drel.core.models import RequestLog
from drel.core.models import ResponseLog
from drel.core.utils import build_log_type


class BaseFullRequestLogBuilder:
    def __init__(self, type_prefix: Optional[str] = None):
        self.type_prefix = type_prefix

    def __call__(self, request: Any, response: Any) -> FullRequestLog:
        return FullRequestLog(
            type=build_log_type("request", self.type_prefix),
            request=self.request_to_log(request),
            response=self.response_to_log(response),
        )

    def request_to_log(self, request: Any) -> RequestLog:
        raise NotImplementedError()

    def response_to_log(self, response: Any) -> ResponseLog:
        raise NotImplementedError()