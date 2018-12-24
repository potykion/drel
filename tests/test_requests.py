import os

import pytest
import responses
from requests import Request
from requests import Session

from drel.core.config import ELASTIC_SEARCH_RUN_TESTS
from drel.core.es import get_from_es
from drel.core.models import FullRequestLog
from drel.core.models import RequestLog
from drel.core.models import ResponseLog
from drel.requests.api import RequestsFullRequestLogBuilder, log


def test_request_with_data_to_log(log_builder):
    request = Request("POST", "https://httpbin.org/post", data={"param1": "value"})
    assert log_builder.request_to_log(request) == RequestLog(
        url=request.url, data=request.data, headers=request.headers
    )


def test_request_with_json_to_log(log_builder):
    request = Request("POST", "https://httpbin.org/post", json={"param1": "value"})
    assert log_builder.request_to_log(request) == RequestLog(
        url=request.url, data=request.json, headers=request.headers
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
    response = session.send(requests_request.prepare())

    assert log_builder.response_to_log(response) == ResponseLog(
        response_params["json"], response_params["status"]
    )


@responses.activate
def test_500_response_to_log(log_builder, requests_request):
    response_params = {'body': "Internal server error", 'status': 500}
    responses.add("POST", requests_request.url, **response_params)

    session = Session()
    response = session.send(requests_request.prepare())

    assert log_builder.response_to_log(response) == ResponseLog(
        {"content": response_params["body"]}, response.status_code
    )


def test_full_request_to_log(
    freezer, log_builder: RequestsFullRequestLogBuilder, requests_request, requests_response
):
    actual_log = log_builder(requests_request, requests_response)
    expected_log = FullRequestLog(
        log_builder.request_to_log(requests_request),
        log_builder.response_to_log(requests_response),
    )
    assert actual_log == expected_log


@pytest.mark.skipif(
    not ELASTIC_SEARCH_RUN_TESTS,
    reason="Set ELASTIC_SEARCH_RUN_TESTS env to enable Elastic Search tests",
)
def test_requests_log_insert_to_es(
    freezer, test_es_index, requests_request, requests_response, serialized_full_request_log,
):
    doc_id = log(requests_request, requests_response)
    actual_full_request_log = get_from_es(doc_id)
    assert actual_full_request_log == serialized_full_request_log


