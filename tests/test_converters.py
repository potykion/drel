import pytest
from requests import Request, PreparedRequest

from drel.converters import requests_request_to_log_entry
from drel.models import LogEntry
from drel.utils import to_json


@pytest.fixture
def post_requests_request_with_form_data():
    request = Request(
        "POST",
        "https://httpbin.org/post",
        data={"param1": "value"},
    )
    return request.prepare()


@pytest.fixture
def post_requests_request_with_json_data():
    request = Request(
        "POST",
        "https://httpbin.org/post",
        json={"param1": "value"},
    )
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
