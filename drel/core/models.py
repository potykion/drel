from datetime import datetime
from typing import Dict

import attr

from drel.core import config
from drel.core.config import request_id_storage


@attr.s(auto_attribs=True)
class RequestLog:
    url: str
    data: Dict
    headers: Dict = attr.ib(factory=dict)


@attr.s(auto_attribs=True)
class ResponseLog:
    data: Dict
    status: int


@attr.s(auto_attribs=True)
class FullRequestLog:
    request: RequestLog
    response: ResponseLog
    type: str = config.DEFAULT_LOG_TYPE
    request_id: str = attr.ib(default=request_id_storage.request_id)
    timestamp: datetime = attr.ib(factory=lambda: datetime.utcnow())
    app: str = attr.ib(default=config.APPLICATION)
    user: Dict = attr.ib(factory=dict)
    stats: Dict = attr.ib(factory=dict)
