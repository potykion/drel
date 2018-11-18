from datetime import datetime

import attr
from freezegun import freeze_time

from drel.models import LogEntry


def test_log_entry_creation():
    data = {"request_id": "request-id", "type": "request", "content": {"path": "/index"}}
    datetime_ = datetime(2018, 11, 15)

    with freeze_time(datetime_):
        entry = LogEntry(**data)

    assert attr.asdict(entry) == {**data, "timestamp": datetime_}
