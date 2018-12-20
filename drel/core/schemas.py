from typing import Dict

from marshmallow import Schema, fields, post_dump

from drel.core.models import DEFAULT_LOG_TYPE


class RequestLogSchema(Schema):
    class Meta:
        fields = ("url", "data", "headers")


class ResponseLogSchema(Schema):
    class Meta:
        fields = ("data", "status")


class FullRequestLogSchema(Schema):
    request = fields.Nested(RequestLogSchema)
    response = fields.Nested(ResponseLogSchema)

    class Meta:
        fields = ("type", "request", "response", "request_id", "timestamp", "app")

    @post_dump
    def append_type(self, data: Dict) -> Dict:
        type_ = data["type"]
        if type_ == DEFAULT_LOG_TYPE:
            return data

        data[f"{type_}_request"] = data.pop("request")
        data[f"{type_}_response"] = data.pop("response")

        return data
