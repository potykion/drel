from typing import Any, Optional, Dict

from drel.core import config
from .models import FullRequestLog, RequestLog, ResponseLog


class BaseFullRequestLogBuilder:
    def __init__(self, type: Optional[str] = None, user: Any = None):
        self.type = type or config.DEFAULT_LOG_TYPE
        self.user = user
        self.request_log: Optional[RequestLog] = None
        self.response_log: Optional[ResponseLog] = None

    def __call__(
        self,
        request: Any = None,
        response: Any = None,
        user: Any = None,
        duration: Optional[float] = None,
    ) -> FullRequestLog:
        request_log = self.request_log or (self.request_to_log(request) if request else None)
        assert request_log

        response_log = self.response_log or (self.response_to_log(response) if response else None)
        assert response_log

        log = FullRequestLog(
            request=request_log,
            response=response_log,
            type=self.type,
            user=self._serialize_user(user or self.user),
        )

        if duration:
            log.stats["duration"] = duration

        return log

    def _serialize_user(self, user: Any) -> Dict:
        user_data, _ = config.USER_SERIALIZER.dump(user)
        return user_data

    def request_to_log(self, request: Any) -> RequestLog:
        request_log = RequestLog(
            self._get_request_url(request),
            self._get_request_data(request),
            self._get_request_headers(request),
        )
        self.request_log = request_log
        return request_log

    def response_to_log(self, response: Any) -> ResponseLog:
        response_log = ResponseLog(
            self._get_response_data(response), self._get_response_status(response)
        )
        self.response_log = response_log
        return response_log

    def _get_request_url(self, request: Any) -> str:
        raise NotImplementedError()

    def _get_request_data(self, request: Any) -> Dict:
        raise NotImplementedError()

    def _get_request_headers(self, request: Any) -> Dict:
        raise NotImplementedError()

    def _get_response_data(self, response: Any) -> Dict:
        raise NotImplementedError()

    def _get_response_status(self, response: Any) -> int:
        raise NotImplementedError()
