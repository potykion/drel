from datetime import datetime
from typing import Dict, Tuple, Any, Callable

from django.http import HttpRequest
from marshmallow import Schema, fields

from drel.utils import datetime_to_week_range


def handle_es_exception(index: str, doc: Dict, exception: Exception) -> None:
    raise exception


class EmailUserSchema(Schema):
    email = fields.Email()


def get_index_name() -> str:
    week_start, week_end = datetime_to_week_range()
    return f"logs-{week_start.date()}-{week_end.date()}"


def log_only_post(request: HttpRequest) -> bool:
    return request.method != "POST"


def timeit(func: Callable, *args: Any, **kwargs: Any) -> Tuple[Any, float]:
    start = datetime.now()
    result = func(*args, **kwargs)
    end = datetime.now()
    took_seconds = (end - start).total_seconds()
    return result, took_seconds
