# Changelog

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