from typing import Dict
from typing import Optional

from requests import PreparedRequest
from requests import Response

from drel.core.builders import BaseFullRequestLogBuilder
from drel.core.models import RequestLog
from drel.core.models import ResponseLog
from drel.core.utils import log_to_es
from drel.core.utils import to_json


def log(request: PreparedRequest, response: Response, type_prefix: Optional[str] = None) -> bool:
    log_entry = RequestsFullRequestLogBuilder(type_prefix)(request, response)

    return log_to_es(log_entry)


class RequestsFullRequestLogBuilder(BaseFullRequestLogBuilder):
    def request_to_log(self, request: PreparedRequest) -> RequestLog:
        assert request.url
        # todo works incorrect for form data
        return RequestLog(request.url, to_json(request.body), dict(request.headers))

    def response_to_log(self, response: Response) -> ResponseLog:
        data = self.__get_response_data(response)
        return ResponseLog(data, response.status_code)

    def __get_response_data(self, response: Response) -> Dict:
        try:
            return response.json()
        except ValueError:
            return to_json(response.content)
