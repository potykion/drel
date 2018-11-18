import json
from typing import Union, Dict


def to_json(str_: Union[str, bytes, None]) -> Dict:
    """
    >>> to_json('{"key":"value"}')
    {'key': 'value'}
    >>> to_json("sam")
    {'content': 'sam'}
    >>> to_json(b"sam")
    {'content': 'sam'}
    """
    str_ = to_str(str_)

    try:
        return json.loads(str_)
    except (ValueError, TypeError):
        return {"content": str_}


def to_str(str_or_bytes: Union[str, bytes, None]) -> str:
    """
    >>> to_str(b"ass")
    'ass'
    >>> to_str("ass")
    'ass'
    >>> to_str(None)
    ''
    """
    if str_or_bytes is None:
        return ""

    if isinstance(str_or_bytes, bytes):
        return str_or_bytes.decode("utf-8")

    return str_or_bytes
