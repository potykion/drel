# drel

Django request ElasticSearch logging

## [WIP] Requests support

```pydocstring
>>> import requests
>>> response = requests.post("https://httpbin.org/post", {"param1": "value1"})
>>> from drel.requests import log
>>> log(response.request, response)
```

This will insert request and response to ElasticSearch index called `logs-{week_start}-{week_end}`:

```json
{
    "type": "request",
    "request": {
      "url": "https://httpbin.org/post",
      "data": {"param1": "value1"},
      "headers": {}
    },
    "response": {
      "status_code": 200,
      "data": {"args": {}, "data": "", "files": {}, "form": {"param1": "value1"}, "headers": {"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Content-Length": "13", "Content-Type": "application/x-www-form-urlencoded", "Host": "httpbin.org", "User-Agent": "python-requests/2.19.1"}, "json": null, "origin": "130.193.67.76", "url": "https://httpbin.org/post"}
    },
    "app": "sample_app",
    "request_id": "2180930f-859b-4aef-8770-17107fff1170"
}
```



