from datetime import datetime
from typing import Dict

import attr


@attr.s(auto_attribs=True)
class LogEntry:
    request_id: str
    type: str
    content: Dict
    datetime: datetime
