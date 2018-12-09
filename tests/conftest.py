import pytest
from requests import Request
from responses import Response

from drel.core.schemas import FullRequestLogSchema
from drel.requests.api import RequestsFullRequestLogBuilder


@pytest.fixture()
def log_builder():
    return RequestsFullRequestLogBuilder()


@pytest.fixture()
def requests_request():
    return Request("POST", "https://httpbin.org/post", data={"param1": "value"})


@pytest.fixture()
def requests_response(requests_request):
    return Response("POST", requests_request.url, json={"status": "success"}, status=200)


@pytest.fixture()
def full_request_log_schema():
    return FullRequestLogSchema()
