from datetime import datetime
from typing import Dict

import attr

from drel.config import request_id_storage


@attr.s(auto_attribs=True)
class LogEntry:
    type: str
    content: Dict
    request_id: str = attr.ib(default=request_id_storage.request_id)
    timestamp: datetime = attr.ib(factory=lambda: datetime.now())


@attr.s(auto_attribs=True)
class RequestLog:
    url: str
    data: Dict
    headers: Dict = attr.ib(factory=dict)


@attr.s(auto_attribs=True)
class ResponseLog:
    status_code: int
    data: Dict
