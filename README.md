# drel

Django request ElasticSearch logging

## Django support

To log every django request insert LoggingMiddleware before AuthenticationMiddleware:

```python
# settings.py

MIDDLEWARE = [
    ...,
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "drel.django.LoggingMiddleware",
    ...
]
```

This will insert request and response info to Elastic Search index called `logs-{week_start}-{week_end}` in following format: 

```json
{
    "timestamp": "2018-12-09 02:22:22",
    "type": "default",
    "request": {
      "url": "https://httpbin.org/post",
      "data": {"param1": "value1"},
      "headers": {}
    },
    "response": {
      "status": 200,
      "data": {"args": {}, "data": "", "files": {}, "form": {"param1": "value1"}, "headers": {"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Content-Length": "13", "Content-Type": "application/x-www-form-urlencoded", "Host": "httpbin.org", "User-Agent": "python-requests/2.19.1"}, "json": null, "origin": "130.193.67.76", "url": "https://httpbin.org/post"}
    },
    "app": "default",
    "request_id": "2180930f-859b-4aef-8770-17107fff1170"
}
```

## Requests support

To log [requests](http://docs.python-requests.org/en/master/) request and response data use `drel.requests.log` function: 

```pydocstring
>>> from drel.requests import post, log
>>> request, response = post("https://httpbin.org/post", {"param1": "value1"})
>>> log(request, response)
```

## Configuration

To change settings override `config` module values:

```python
from drel import config

config.APPLICATION = "django_app"
``` 


### Sample Django configuration

```python
from django.http import HttpRequest
from drel.core import config
from drel.django import mail_admins_on_es_exception

def ignore_logging_handler(request: HttpRequest) -> bool:
    return any([
        request.path == "/api/register_device/",
        request.method != "POST",
    ])


config.ELASTIC_SEARCH_EXCEPTION_HANDLER = mail_admins_on_es_exception
config.INDEX_NAME_GETTER = lambda: "django_app_2019-01-01"
config.APPLICATION = "django_app"
config.IGNORE_LOGGING_HANDLER = ignore_logging_handler
```

This configuration:
 
 - mail admins on Elastic Search index exception
 - ignore logging non-POST and /api/register_device/ requests
 - insert docs to django_app_2019-01-01 index
 - application field = django_app
