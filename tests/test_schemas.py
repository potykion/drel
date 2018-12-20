import pytest
from requests import Request

from drel.core import FullRequestLog
from drel.core.schemas import FullRequestLogSchema
from drel.utils import format_datetime


@pytest.fixture()
def full_request_log_schema():
    return FullRequestLogSchema()


def test_full_request_log_to_json(
        requests_request: Request, full_request_log, requests_response, full_request_log_schema
):
    json_, _ = full_request_log_schema.dump(full_request_log)
    assert json_ == {
        "type": full_request_log.type,
        "request": {
            "url": requests_request.url,
            "data": requests_request.data or requests_request.json,
            "headers": requests_request.headers,
        },
        "response": {"status": requests_response.status_code, "data": requests_response.json()},
        "app": full_request_log.app,
        "request_id": full_request_log.request_id,
        "timestamp": format_datetime(full_request_log.timestamp),
    }


def test_full_request_log_with_non_default_type(
        full_request_log_with_type: FullRequestLog, full_request_log_schema: FullRequestLogSchema
):
    type_ = full_request_log_with_type.type

    json_, _ = full_request_log_schema.dump(full_request_log_with_type)

    assert json_["type"] == type_
    assert f"{type_}_request" in json_
    assert f"{type_}_response" in json_
