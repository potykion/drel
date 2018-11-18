import json
from typing import Any, Dict


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
