from functools import partial
from typing import Callable
from typing import Dict

from marshmallow.schema import BaseSchema

from drel.core import config
from drel.core.models import FullRequestLog
from drel.core.schemas import FullRequestLogSchema


def log_to_es(log: FullRequestLog) -> bool:
    schema: BaseSchema = FullRequestLogSchema()
    doc, _ = schema.dump(log)
    return write_to_es(doc)


write_to_es: Callable[[Dict], bool] = partial(
    config.ELASTIC_SEARCH.index, config.INDEX_NAME_GETTER(), "default"
)
