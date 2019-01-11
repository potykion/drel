import uuid
from typing import Dict, Callable, Any

from django.core.mail import mail_admins
from django.http import HttpRequest, HttpResponse, RawPostDataException

from drel.core import BaseFullRequestLogBuilder, log_to_es, config
from drel.core.config import request_id_storage
from drel.utils import to_json


class LoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if config.IGNORE_LOGGING_HANDLER(request):
            return self.get_response(request)

        request_id_storage.request_id = str(uuid.uuid4())

        builder = DjangoFullRequestLogBuilder()

        builder.request_to_log(request)

        response = self.get_response(request)
        builder.response_to_log(response)

        log_entry = builder(user=request.user)
        log_to_es(log_entry)

        return response


class DjangoFullRequestLogBuilder(BaseFullRequestLogBuilder):
    def _get_request_url(self, request: Any) -> str:
        return request.get_full_path()

    def _get_request_data(self, request: Any) -> Dict:
        try:
            return request.POST.dict() or to_json(request.body)
        except RawPostDataException:
            return {}

    def _get_request_headers(self, request: Any) -> Dict:
        return {key: value for key, value in request.META.items() if key.startswith("HTTP")}

    def _get_response_data(self, response: Any) -> Dict:
        return to_json(response.content)

    def _get_response_status(self, response: Any) -> int:
        return response.status_code


def mail_admins_on_es_exception(index: str, doc: Dict, exception: Exception) -> None:
    message = _build_exception_message(index, doc, exception)
    mail_admins("Logging to Elastic Search failed", message)


def _build_exception_message(index: str, doc: Dict, exception: Exception) -> str:
    return f"""Index: {index}

Doc to insert: {doc}

Exception class: {exception.__class__}

Exception details: {exception}"""
