from typing import Dict
from typing import Optional

import attr
from requests import PreparedRequest
from requests import Response

from drel.models import LogEntry, RequestLog
from drel.models import ResponseLog
from drel.utils import to_json


def requests_request_to_log_entry(
    request: PreparedRequest, type_prefix: Optional[str] = None
) -> LogEntry:
    assert request.url

    type_ = _build_log_type("request", type_prefix)

    request_log = RequestLog(request.url, to_json(request.body), dict(request.headers))

    return LogEntry(type=type_, content=attr.asdict(request_log))


def requests_response_to_log_entry(
    response: Response, type_prefix: Optional[str] = None
) -> LogEntry:
    type_ = _build_log_type("response", type_prefix)
    body = _get_response_data(response)

    request_log = ResponseLog(response.status_code, body)

    return LogEntry(type=type_, content=attr.asdict(request_log))


def _get_response_data(response: Response) -> Dict:
    try:
        return response.json()
    except ValueError:
        return to_json(response.content)


def _build_log_type(base_type: str, type_prefix: Optional[str] = None) -> str:
    if type_prefix:
        return f"{type_prefix}_{base_type}"

    return base_type
