from typing import Dict

from marshmallow import Schema, fields, post_dump

from drel.core import config


class RequestLogSchema(Schema):
    class Meta:
        fields = ("url", "data", "headers")


class ResponseLogSchema(Schema):
    class Meta:
        fields = ("data", "status")


class StatsSchema(Schema):
    class Meta:
        fields = ("duration",)


class FullRequestLogSchema(Schema):
    request = fields.Nested(RequestLogSchema)
    response = fields.Nested(ResponseLogSchema)
    timestamp = fields.DateTime()
    user = fields.Nested(config.USER_SERIALIZER)
    stats = fields.Nested(StatsSchema)

    class Meta:
        fields = (
            "type",
            "request",
            "response",
            "request_id",
            "timestamp",
            "app",
            "user",
            "stats",
        )

    @post_dump
    def append_type(self, data: Dict) -> Dict:
        type_ = data["type"]
        if type_ == config.DEFAULT_LOG_TYPE:
            return data

        data[f"{type_}_request"] = data.pop("request")
        data[f"{type_}_response"] = data.pop("response")

        return data

    @post_dump()
    def drop_blank_fields(self, data: Dict) -> Dict:
        return {field: value for field, value in data.items() if value}
