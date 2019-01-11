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
        if self.request_log:
            request_log = self.request_log
        else:
            assert request is not None
            request_log = self.request_to_log(request)

        if self.response_log:
            response_log = self.response_log
        else:
            assert response is not None
            response_log = self.response_to_log(response)

        log = FullRequestLog(
            request=request_log,
            response=response_log,
            type=self.type,
            user=self._serialize_user(user or self.user),
        )

        if duration is not None:
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
