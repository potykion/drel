import responses
from requests import Request
from requests import Session

from drel.core.utils import format_datetime
from drel.requests.api import RequestsFullRequestLogBuilder


@responses.activate
def test_full_request_log_to_json(
    log_builder: RequestsFullRequestLogBuilder,
    requests_request: Request,
    requests_response,
    full_request_log_schema,
):
    responses.add(requests_response)

    session = Session()
    response = session.send(requests_request.prepare())

    # todo FullRequestLog as fixture
    request_log = log_builder(requests_request, response)

    json_, _ = full_request_log_schema.dump(request_log)
    assert json_ == {
        "type": request_log.type,
        "request": {
            "url": requests_request.url,
            "data": requests_request.data or requests_request.json,
            "headers": requests_request.headers,
        },
        "response": {"status": response.status_code, "data": response.json()},
        "app": request_log.app,
        "request_id": request_log.request_id,
        "timestamp": format_datetime(request_log.timestamp),
    }
