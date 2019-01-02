import json

import pytest
from django.http import JsonResponse
from django.test import Client, RequestFactory
from django.urls import reverse

from drel.core import RequestLog, ResponseLog, config
from drel.core.es import get_es_docs
from drel.django.api import DjangoFullRequestLogBuilder


@pytest.fixture()
def log_builder():
    return DjangoFullRequestLogBuilder()


def test_post_request_with_form_data(rf: RequestFactory, log_builder: DjangoFullRequestLogBuilder):
    data = {"field": "value"}

    request = rf.post(reverse("success"), data)

    log = log_builder.request_to_log(request)
    assert log == RequestLog(request.get_full_path(), data, {"HTTP_COOKIE": ""})


def test_post_request_with_json_data(rf: RequestFactory, log_builder: DjangoFullRequestLogBuilder):
    data = {"field": "value"}

    request = rf.post(reverse("success"), json.dumps(data), content_type="application/json")

    log = log_builder.request_to_log(request)
    assert log == RequestLog(request.get_full_path(), data, {"HTTP_COOKIE": ""})


def test_response_data(client: Client, log_builder: DjangoFullRequestLogBuilder):
    response: JsonResponse = client.post(reverse("success"))
    log = log_builder.response_to_log(response)
    assert log == ResponseLog({"status": "success", "body": None}, 200)


def test_500_response(client: Client, log_builder: DjangoFullRequestLogBuilder):
    response: JsonResponse = client.post(reverse("server_error"))
    log = log_builder.response_to_log(response)
    assert log == ResponseLog({"content": "Internal server error."}, 500)


@pytest.mark.skipif(
    not config.ELASTIC_SEARCH_RUN_TESTS,
    reason="Set ELASTIC_SEARCH_RUN_TESTS env to enable Elastic Search tests",
)
def test_logging_middleware_with_post_data(freezer, test_es_index, client, log_builder, full_request_log_schema, rf: RequestFactory):
    data = {"field": "django"}

    request = rf.post(reverse("success"), data)
    response: JsonResponse = client.post(reverse("success"), data)

    log = log_builder(request, response)

    expected, _ = full_request_log_schema.dump(log)
    actual = get_es_docs()[0]

    assert expected == actual


@pytest.mark.skipif(
    not config.ELASTIC_SEARCH_RUN_TESTS,
    reason="Set ELASTIC_SEARCH_RUN_TESTS env to enable Elastic Search tests",
)
def test_logging_middleware_with_json_data(freezer, test_es_index, client, log_builder, full_request_log_schema, rf: RequestFactory):
    data = {"field": "django"}

    request = rf.post(reverse("success"), json.dumps(data), content_type="application/json")

    response: JsonResponse = client.post(reverse("success"), json.dumps(data), content_type="application/json")

    log = log_builder(request, response)

    expected, _ = full_request_log_schema.dump(log)
    actual = get_es_docs()[0]

    assert expected == actual

@pytest.mark.skipif(
    not config.ELASTIC_SEARCH_RUN_TESTS,
    reason="Set ELASTIC_SEARCH_RUN_TESTS env to enable Elastic Search tests",
)
def test_non_post_requests_logging(client, test_es_index, ):
    client.get(reverse("success"))
    assert not len(get_es_docs())
