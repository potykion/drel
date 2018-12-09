from marshmallow import Schema, fields


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
