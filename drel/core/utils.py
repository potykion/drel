from typing import Dict

from marshmallow import Schema, fields

from drel.utils import datetime_to_week_range


def handle_es_exception(index: str, doc: Dict, exception: Exception) -> None:
    raise exception


class EmailUserSchema(Schema):
    email = fields.Email()


def get_index_name() -> str:
    week_start, week_end = datetime_to_week_range()
    return f"logs-{week_start.date()}-{week_end.date()}"
