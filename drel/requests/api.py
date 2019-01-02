from typing import Any, Dict, Tuple, Optional

import requests
from requests import Response, Request

from drel.core import BaseFullRequestLogBuilder, log_to_es
from drel.utils import to_json


def log(request: Request, response: Response, **builder_kwargs: Any) -> Optional[str]:
    log_entry = RequestsFullRequestLogBuilder(**builder_kwargs)(request, response)

    return log_to_es(log_entry)


class RequestsFullRequestLogBuilder(BaseFullRequestLogBuilder):
    def _get_request_url(self, request: Any) -> str:
        assert request.url
        return request.url

    def _get_request_data(self, request: Any) -> Dict:
        return request.data or request.json

    def _get_request_headers(self, request: Any) -> Dict:
        return dict(request.headers)

    def _get_response_data(self, response: Any) -> Dict:
        try:
            return response.json()
        except ValueError:
            return to_json(response.content)

    def _get_response_status(self, response: Any) -> int:
        return response.status_code


def post(*args: Any, **kwargs: Any) -> Tuple[Request, Response]:
    request = requests.Request("POST", *args, **kwargs)
    session = requests.Session()
    response = session.send(request.prepare())
    return request, response


def get(*args: Any, **kwargs: Any) -> Tuple[Request, Response]:
    request = requests.Request("GET", *args, **kwargs)
    session = requests.Session()
    response = session.send(request.prepare())
    return request, response
