# drel

Django request ElasticSearch logging

## Django support

To log every django request insert logging middleware before AuthenticationMiddleware:

```python
# settings.py

MIDDLEWARE = [
    ...,
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "drel.django.LoggingMiddleware",
]

```

To change settings override config module values:

```python
# settings.py

from drel import config

config.APPLICATION = "django_app"
``` 


## Requests support

```pydocstring
>>> from drel.requests import post, log
>>> request, response = post("https://httpbin.org/post", {"param1": "value1"})
>>> log(request, response)
```

This will insert request and response to ElasticSearch index called `logs-{week_start}-{week_end}`:

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



