from django.http import HttpResponse, HttpRequest, JsonResponse


def success_view(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"status": "success"})
