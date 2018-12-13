import json

import pytest
from django.http import JsonResponse, HttpRequest
from django.test import Client
from django.urls import reverse

from drel.core import RequestLog, ResponseLog
from drel.django.api import DjangoFullRequestLogBuilder


@pytest.fixture()
def log_builder():
    return DjangoFullRequestLogBuilder()


def test_post_request_with_form_data(client: Client, log_builder: DjangoFullRequestLogBuilder):
    data = {"field": "value"}
    response: JsonResponse = client.post(reverse("success"), data)
    request: HttpRequest = response.wsgi_request
    log = log_builder.request_to_log(request)
    assert log == RequestLog(request.get_full_path(), data, {"HTTP_COOKIE": ""})


def test_post_request_with_json_data(client: Client, log_builder: DjangoFullRequestLogBuilder):
    data = {"field": "value"}
    response: JsonResponse = client.post(reverse("success"), json.dumps(data), content_type="application/json")
    request: HttpRequest = response.wsgi_request
    log = log_builder.request_to_log(request)
    assert log == RequestLog(request.get_full_path(), data, {"HTTP_COOKIE": ""})


def test_response_data(client: Client, log_builder: DjangoFullRequestLogBuilder):
    response: JsonResponse = client.post(reverse("success"))
    log = log_builder.response_to_log(response)
    assert log == ResponseLog({"status": "success"}, 200)


def test_500_response(client: Client, log_builder: DjangoFullRequestLogBuilder):
    response: JsonResponse = client.post(reverse("server_error"))
    log = log_builder.response_to_log(response)
    assert log == ResponseLog({"content": "Internal server error."}, 500)
