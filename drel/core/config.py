import threading
import uuid
from typing import Callable

from elasticsearch import Elasticsearch

from drel.core.utils import datetime_to_week_range

request_id_storage = threading.local()
request_id_storage.request_id = str(uuid.uuid4())

ELASTIC_SEARCH: Elasticsearch = Elasticsearch()

APPLICATION: str = "default"


def get_index_name() -> str:
    week_start, week_end = datetime_to_week_range()
    return f"logs-{week_start}-{week_end}"


INDEX_NAME_GETTER: Callable[[], str] = get_index_name
