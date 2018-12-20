import pytest
import responses
from requests import Request, Session
from responses import Response

from drel.requests.api import RequestsFullRequestLogBuilder


@pytest.fixture()
def log_builder():
    return RequestsFullRequestLogBuilder()

@pytest.fixture()
def log_builder_with_type():
    return RequestsFullRequestLogBuilder(type_="requests")


@pytest.fixture()
def requests_request():
    return Request("POST", "https://httpbin.org/post", data={"param1": "value"})


@pytest.fixture()
def requests_response(requests_request):
    with responses.RequestsMock() as responses_:
        responses_.add(
            Response("POST", requests_request.url, json={"status": "success"}, status=200)
        )

        session = Session()
        response = session.send(requests_request.prepare())

        return response


@pytest.fixture()
def full_request_log(log_builder, requests_request, requests_response):
    return log_builder(requests_request, requests_response)


@pytest.fixture()
def full_request_log_with_type(log_builder_with_type, requests_request, requests_response):
    return log_builder_with_type(requests_request, requests_response)
