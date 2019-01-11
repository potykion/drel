# Changelog

## 0.5.1 - 2019-01-11

### Fixed 

- Merge 0.4.3 and 0.5.0 (:


## 0.5.0 - 2019-01-11

### Added

- drel.core.builders.BaseFullRequestLogBuilder: user can be passed into dunder call method
- drel.core.schemas.FullRequestLogSchema: stats - dict with request stats (like duration)
- drel.requests.api.log: duration kwarg
- drel.django.api.LoggingMiddleware: duration logging 

### Fixed

- drel.django.LoggingMiddleware: log user after request processing 


## 0.4.3 - 2019-01-03 

### Fixed

- Fix logging non 200 status requests.Response's

## 0.4.2 - 2019-01-02 

### Fixed 

- Fix logging Django requests with json data

## 0.4.1 - 2019-01-01

### Fixed

- Load ELASTIC_SEARCH_RUN_TESTS from config instead of absolute import
- drel.django.LoggingMiddleware: Refresh request id on every request 

## 0.4.0 - 2018-12-31

### Added

- drel.requests.get - like requests.get, but returns request, response tuple

### Fixed

- Fix non-UTC datetime default for FullRequestLog.timestamp

## 0.3.0 - 2018-12-31

### Added 

- drel.django.mail_admins_on_es_exception - Send Elastic Search exception info to Django ADMINS

    Usage: 
    
    ```python
    from drel import config
    from drel.django import mail_admins_on_es_exception
    
    config.ELASTIC_SEARCH_EXCEPTION_HANDLER = mail_admins_on_es_exception
    ```

### Fixed

- Set ELASTIC_SEARCH_RUN_TESTS == True by default due to logging should be enabled in production by default 
- Fix versions in setup.py

## 0.2.0 - 2018-12-24

### Added 

- django.LoggingMiddleware: Ignore logging some requests via config.IGNORE_LOGGING_HANDLER (by default ignore non POST requests)
- es.get_index_docs: return empty list on index not found

### Fixed

- Fix Elastic Search tests run on ELASTIC_SEARCH_RUN_TESTS disabled

## 0.1.1 - 2018-12-21

### Changed  

- Update README

## 0.1.0 - 2018-12-21

### Added 

- Django logging middleware
- Requests request/response logging
- FullRequestLog general fields: type, app, timestamp, request_id
- FullRequestLog.request = {url, data, headers}
- FullRequestLog.response = {data, status}
- FullRequestLog.user = {email} (configurable via config.USER_SERIALIZER)
- Append FullRequestLog.type to request, response fields in FullRequestLog json if FullRequestLog.type != DEFAULT_LOG_TYPE
- Drop blank fields from FullRequestLog json
- Elastic Search index generation = current week range (configurable via config.INDEX_NAME_GETTER)
- Elastic Search exception handling = raising Exception (configurable via config.ELASTIC_SEARCH_EXCEPTION_HANDLER)
- Configurable Elastic Search instance via ELASTIC_SEARCH_HOST, ELASTIC_SEARCH_PORT envs
- Configurable Elastic Search index refresh via ELASTIC_SEARCH_REFRESH_ON_INSERT env