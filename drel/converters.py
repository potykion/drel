from typing import Optional

import attr
from requests import PreparedRequest

from drel.models import LogEntry, RequestLog
from drel.utils import to_json


def requests_request_to_log_entry(
    request: PreparedRequest, type_prefix: Optional[str] = None
) -> LogEntry:
    assert request.url

    if type_prefix:
        type_ = f"{type_prefix}_request"
    else:
        type_ = "request"

    request_log = RequestLog(request.url, to_json(request.body), dict(request.headers))

    return LogEntry(type=type_, content=attr.asdict(request_log))
