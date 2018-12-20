import os
import threading
import uuid
from typing import Callable

from elasticsearch import Elasticsearch

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

APPLICATION: str = "default"


def get_index_name() -> str:
    week_start, week_end = datetime_to_week_range()
    return f"logs-{week_start.date()}-{week_end.date()}"


INDEX_NAME_GETTER: Callable[[], str] = get_index_name

DOC_TYPE = "default"
