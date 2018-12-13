from django.http import HttpResponse, HttpRequest, JsonResponse


def success_view(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"status": "success"})


def server_error_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Internal server error.", status=500)
