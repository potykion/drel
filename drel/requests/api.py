from typing import Any, Dict, Optional, Tuple

import requests
from requests import Response, Request

from drel.core import BaseFullRequestLogBuilder, RequestLog, ResponseLog, log_to_es
from drel.utils import to_json


def log(request: Request, response: Response, type_: Optional[str] = None) -> str:
    log_entry = RequestsFullRequestLogBuilder(type_)(request, response)

    return log_to_es(log_entry)


class RequestsFullRequestLogBuilder(BaseFullRequestLogBuilder):
    def request_to_log(self, request: Request) -> RequestLog:
        assert request.url
        return RequestLog(request.url, request.data or request.json, dict(request.headers))

    def response_to_log(self, response: Response) -> ResponseLog:
        data = self.__get_response_data(response)
        return ResponseLog(data, response.status_code)

    def __get_response_data(self, response: Response) -> Dict:
        try:
            return response.json()
        except ValueError:
            return to_json(response.content)


def post(*args: Any, **kwargs: Any) -> Tuple[Request, Response]:
    request = requests.Request("POST", *args, **kwargs)
    session = requests.Session()
    response = session.send(request.prepare())
    return request, response
