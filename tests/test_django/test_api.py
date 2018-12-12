from django.http import JsonResponse
from django.test import Client
from django.urls import reverse


def test_get_response_data(client: Client):
    response: JsonResponse = client.post(reverse("success"))
    assert response.json() == {"status": "success"}
