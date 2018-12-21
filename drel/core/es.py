from operator import itemgetter
from typing import Dict, Optional, List

from marshmallow.schema import BaseSchema

from drel.core import config
from drel.core.models import FullRequestLog
from drel.core.schemas import FullRequestLogSchema


def log_to_es(log: FullRequestLog) -> str:
    schema: BaseSchema = FullRequestLogSchema()
    doc, _ = schema.dump(log)
    return write_to_es(doc)


def write_to_es(doc: Dict) -> str:
    doc = config.ELASTIC_SEARCH.index(
        config.INDEX_NAME_GETTER(),
        config.DOC_TYPE,
        doc,
        refresh=config.ELASTIC_SEARCH_REFRESH_ON_INSERT,
    )
    return doc["_id"]


def get_from_es(doc_id: str) -> Dict:
    doc = config.ELASTIC_SEARCH.get(config.INDEX_NAME_GETTER(), config.DOC_TYPE, doc_id)
    return doc["_source"]


def get_es_docs(index: Optional[str] = None, size: int = 20) -> List[Dict]:
    index = index or config.INDEX_NAME_GETTER()
    result = config.ELASTIC_SEARCH.search(index=index, size=size)
    return list(map(itemgetter("_source"), result["hits"]["hits"]))
