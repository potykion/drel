import json
from datetime import datetime
from datetime import time
from datetime import timedelta
from typing import Any, Dict
from typing import Optional
from typing import Tuple


def to_json(object_: Any) -> Dict:
    """
    >>> to_json('{"key":"value"}')
    {'key': 'value'}
    >>> to_json("sam")
    {'content': 'sam'}
    >>> to_json(b"sam")
    {'content': 'sam'}
    >>> to_json({'key': 'value'})
    {'key': 'value'}
    >>> to_json(b'{"data":"871000010171326_58450_2979766647"}')
    {'data': '871000010171326_58450_2979766647'}
    """
    if isinstance(object_, Dict):
        return object_

    object_ = to_str(object_)

    try:
        return json.loads(object_)
    except (ValueError, TypeError):
        return {"content": object_}


def to_str(object_: Any) -> str:
    """
    >>> to_str(b"ass")
    'ass'
    >>> to_str("ass")
    'ass'
    >>> to_str(None)
    ''
    >>> to_str({"op": "oppa"})
    "{'op': 'oppa'}"
    """
    if object_ is None:
        return ""

    if isinstance(object_, bytes):
        return object_.decode("utf-8")

    return str(object_)


def datetime_to_week_range(datetime_: Optional[datetime] = None) -> Tuple[datetime, datetime]:
    """
    >>> datetime_to_week_range(datetime(2018, 12, 9))
    (datetime.datetime(2018, 12, 3, 0, 0), datetime.datetime(2018, 12, 9, 0, 0))
    """
    datetime_ = datetime_ or datetime.utcnow()
    week_start = datetime_ - timedelta(datetime_.weekday())
    week_start = datetime.combine(week_start, time(0, 0))
    week_end = week_start + timedelta(6)
    return week_start, week_end


def format_datetime(datetime_: datetime) -> str:
    """
    >>> from dateutil.parser import parse
    >>> format_datetime(parse('2018-12-09 02:34:21.996490'))
    '2018-12-09T02:34:21.996490+00:00'
    """
    return f"{datetime_.date()}T{datetime_.time()}+00:00"
