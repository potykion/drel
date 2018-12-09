import pytest
import requests
import responses
from requests import Request
from requests import Session

from drel.core.models import FullRequestLog
from drel.core.models import RequestLog
from drel.core.models import ResponseLog
from drel.core.utils import to_json
from drel.requests.api import RequestsFullRequestLogBuilder


@pytest.mark.parametrize(
    "request",
    [
        Request("POST", "https://httpbin.org/post", data={"param1": "value"}).prepare(),
        Request("POST", "https://httpbin.org/post", json={"param1": "value"}).prepare(),
    ],
)
def test_request_to_log(log_builder, request):
    assert log_builder.request_to_log(request) == RequestLog(
        url=request.url, data=to_json(request.body), headers=request.headers
    )


@responses.activate
@pytest.mark.parametrize(
    "response_params",
    [
        {'json': {"status": "success"}, 'status': 200},
        {'json': {"status": "error"}, 'status': 400},
    ],
)
def test_response_to_log(
    log_builder: RequestsFullRequestLogBuilder, requests_request, response_params
):
    responses.add("POST", requests_request.url, **response_params)

    session = Session()
    response = session.send(requests_request)

    assert log_builder.response_to_log(response) == ResponseLog(
        response_params["json"], response_params["status"]
    )


@responses.activate
def test_500_response_to_log(log_builder, requests_request):
    response_params = {'body': "Internal server error", 'status': 500}
    responses.add("POST", requests_request.url, **response_params)

    session = Session()
    response = session.send(requests_request)

    assert log_builder.response_to_log(response) == ResponseLog(
        {"content": response_params["body"]}, response.status_code
    )


@responses.activate
def test_full_request_to_log(
    log_builder: RequestsFullRequestLogBuilder, requests_request, requests_response
):
    responses.add(requests_response)

    session = Session()
    response = session.send(requests_request)

    actual_log = log_builder(requests_request, response)
    assert actual_log == FullRequestLog(
        "request",
        log_builder.request_to_log(requests_request),
        log_builder.response_to_log(response),
    )
