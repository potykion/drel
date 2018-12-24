import os
import threading
import uuid
from typing import Callable, Dict

from elasticsearch import Elasticsearch
from marshmallow.schema import BaseSchema

from drel.core.utils import handle_es_exception, EmailUserSchema, get_index_name

request_id_storage = threading.local()
request_id_storage.request_id = str(uuid.uuid4())

# Elastic Search options
ELASTIC_SEARCH: Elasticsearch = Elasticsearch(
    hosts=[
        {
            "host": os.getenv("ELASTIC_SEARCH_HOST", "localhost"),
            "port": os.getenv("ELASTIC_SEARCH_PORT", "9200"),
        }
    ]
)

ELASTIC_SEARCH_REFRESH_ON_INSERT = bool(os.getenv("ELASTIC_SEARCH_REFRESH_ON_INSERT"))
ELASTIC_SEARCH_EXCEPTION_HANDLER: Callable[[str, Dict, Exception], None] = handle_es_exception
ELASTIC_SEARCH_DOC_TYPE = "default"

INDEX_NAME_GETTER: Callable[[], str] = get_index_name

# log specific options
APPLICATION = "default"
DEFAULT_LOG_TYPE = "default"
USER_SERIALIZER: BaseSchema = EmailUserSchema()
