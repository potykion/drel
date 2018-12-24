from typing import Dict, Callable

from django.http import HttpRequest, HttpResponse, RawPostDataException

from drel.core import BaseFullRequestLogBuilder, log_to_es, ResponseLog, RequestLog, config
from drel.utils import to_json


class LoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        if config.IGNORE_LOGGING_HANDLER(request):
            return response

        log_entry = DjangoFullRequestLogBuilder(user=request.user)(request, response)
        log_to_es(log_entry)

        return response


class DjangoFullRequestLogBuilder(BaseFullRequestLogBuilder):
    def request_to_log(self, request: HttpRequest) -> RequestLog:
        return RequestLog(
            request.get_full_path(), get_request_data(request), get_request_headers(request)
        )

    def response_to_log(self, response: HttpResponse) -> ResponseLog:
        return ResponseLog(get_response_data(response), response.status_code)


def get_request_data(request: HttpRequest) -> Dict:
    try:
        return request.POST.dict() or to_json(request.body)
    except RawPostDataException:
        return {}


def get_request_headers(request: HttpRequest) -> Dict:
    return {key: value for key, value in request.META.items() if key.startswith("HTTP")}


def get_response_data(response: HttpResponse) -> Dict:
    return to_json(response.content)
