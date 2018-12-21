import os
import threading
import uuid
from typing import Callable, Dict

from elasticsearch import Elasticsearch
from marshmallow import Schema, fields
from marshmallow.schema import BaseSchema

from drel.utils import datetime_to_week_range

request_id_storage = threading.local()
request_id_storage.request_id = str(uuid.uuid4())

ELASTIC_SEARCH: Elasticsearch = Elasticsearch(
    hosts=[
        {
            "host": os.getenv("ELASTIC_SEARCH_HOST", "localhost"),
            "port": os.getenv("ELASTIC_SEARCH_PORT", "9200"),
        }
    ]
)

APPLICATION = "default"


def get_index_name() -> str:
    week_start, week_end = datetime_to_week_range()
    return f"logs-{week_start.date()}-{week_end.date()}"


INDEX_NAME_GETTER: Callable[[], str] = get_index_name


class EmailUserSchema(Schema):
    email = fields.Email()


USER_SERIALIZER: BaseSchema = EmailUserSchema()

DOC_TYPE = "default"

DEFAULT_LOG_TYPE = "default"

ELASTIC_SEARCH_REFRESH_ON_INSERT = bool(os.getenv("ELASTIC_SEARCH_REFRESH_ON_INSERT"))


def handle_es_exception(index: str, doc: Dict, exception: Exception) -> None:
    raise exception


ELASTIC_SEARCH_EXCEPTION_HANDLER: Callable[[str, Dict, Exception], None] = handle_es_exception
