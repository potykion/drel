from typing import Dict

from marshmallow.schema import BaseSchema

from drel.core import config
from drel.core.models import FullRequestLog
from drel.core.schemas import FullRequestLogSchema


def log_to_es(log: FullRequestLog) -> str:
    schema: BaseSchema = FullRequestLogSchema()
    doc, _ = schema.dump(log)
    return write_to_es(doc)


def write_to_es(doc: Dict) -> str:
    return config.ELASTIC_SEARCH.index(config.INDEX_NAME_GETTER(), config.DOC_TYPE, doc)["_id"]


def get_from_es(doc_id: str) -> Dict:
    return config.ELASTIC_SEARCH.get(config.INDEX_NAME_GETTER(), config.DOC_TYPE, doc_id)[
        "_source"
    ]
