import pytest
import requests
import responses
from requests import Request, PreparedRequest
from requests import Session

from drel.converters import requests_request_to_log_entry
from drel.converters import requests_response_to_log_entry
from drel.models import LogEntry
from drel.utils import to_json


@pytest.fixture
def post_requests_request_with_form_data():
    request = Request("POST", "https://httpbin.org/post", data={"param1": "value"})
    return request.prepare()


@pytest.fixture
def post_requests_request_with_json_data():
    request = Request("POST", "https://httpbin.org/post", json={"param1": "value"})
    return request.prepare()


def test_requests_requests_to_log_entry_with_form_data(
        post_requests_request_with_form_data: PreparedRequest
):
    actual_log_entry = requests_request_to_log_entry(post_requests_request_with_form_data)
    assert actual_log_entry == LogEntry(
        "request",
        {
            "url": post_requests_request_with_form_data.url,
            "data": to_json(post_requests_request_with_form_data.body),
            "headers": post_requests_request_with_form_data.headers,
        },
    )


def test_requests_requests_to_log_entry_with_json_data(post_requests_request_with_json_data):
    actual_log_entry = requests_request_to_log_entry(post_requests_request_with_json_data)
    assert actual_log_entry == LogEntry(
        "request",
        {
            "url": post_requests_request_with_json_data.url,
            "data": to_json(post_requests_request_with_json_data.body),
            "headers": post_requests_request_with_json_data.headers,
        },
    )


def test_request_converter_with_request_prefix(post_requests_request_with_form_data):
    actual_log_entry = requests_request_to_log_entry(
        post_requests_request_with_form_data, "httpbin"
    )
    assert actual_log_entry.type == "httpbin_request"


@responses.activate
@pytest.mark.parametrize("response_json, response_status", [
    ({"status": "success"}, 200),
    ({"status": "error"}, 400),
])
def test_requests_response_converter_for_json_response(
        response_json, response_status,
        post_requests_request_with_form_data: PreparedRequest
):
    responses.add(
        responses.POST, post_requests_request_with_form_data.url, status=response_status, json=response_json,
    )

    session = Session()
    response = session.send(post_requests_request_with_form_data)

    assert requests_response_to_log_entry(response) == LogEntry(
        "response", {"data": response_json, "status_code": response_status}
    )


@responses.activate
def test_requests_response_converter_for_non_json_response(
        post_requests_request_with_form_data: PreparedRequest
):
    response_data = "Internal server error"
    response_status = 500

    responses.add(
        responses.POST, post_requests_request_with_form_data.url, status=response_status, body=response_data,
    )

    session = Session()
    response = session.send(post_requests_request_with_form_data)

    assert requests_response_to_log_entry(response) == LogEntry(
        "response", {"data": {"content": response_data}, "status_code": response_status}
    )

