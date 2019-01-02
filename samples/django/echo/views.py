from django.http import HttpResponse, HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request


@api_view(["POST"])
def success_view(request: Request) -> HttpResponse:
    return JsonResponse({"status": "success", "body": request.data.get("field")})


def server_error_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Internal server error.", status=500)
