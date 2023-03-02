from drf_yasg.openapi import Schema
from drf_yasg.openapi import TYPE_OBJECT, TYPE_STRING, TYPE_BOOLEAN, TYPE_INTEGER, TYPE_NUMBER, TYPE_ARRAY, TYPE_FILE
from drf_yasg.openapi import FORMAT_DATE, FORMAT_DOUBLE


class JsonSchema(Schema):

    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_OBJECT, format, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class StringSchema(Schema):

    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_STRING, format, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class BoolSchema(Schema):

    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_BOOLEAN, format, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class IntSchema(Schema):
    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_INTEGER, format, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class DoubleSchema(Schema):
    def __init__(self, description=None, title=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_NUMBER, FORMAT_DOUBLE, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class DateSchema(Schema):
    def __init__(self, description=None, title=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_STRING, FORMAT_DATE, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class FileSchema(Schema):

    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_FILE, format, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class ArrSchema(Schema):
    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_ARRAY, format, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)


class DetailSchema(Schema):
    def __init__(self, content='', description=None, title=None, format=None, enum=None, pattern=None, properties=None,
                 additional_properties=None, required=None, items=None, default=None, read_only=None, **extra):
        if not properties:
            properties = {'detail': StringSchema(content)}
        super().__init__(title, description, TYPE_OBJECT, format, enum, pattern, properties,
                         additional_properties, required, items, default, read_only, **extra)

    @staticmethod
    def token_err():
        return DetailSchema(content='token过期或者无效 禁止访问')


class CodeDetailSchema(Schema):

    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, additional_properties=None,
                 required=None, items=None,
                 default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_OBJECT, format, enum, pattern,
                         {'code': IntSchema('code'), 'detail': StringSchema('详情')},
                         additional_properties, required, items, default, read_only, **extra)


class CodeDataJsonSchema(Schema):
    def __init__(self, description=None, title=None, format=None, enum=None, pattern=None, additional_properties=None,
                 required=None, items=None, default=None, read_only=None, data=None, **extra):
        if data is None:
            data = JsonSchema()
        super().__init__(title, description, TYPE_OBJECT, format, enum, pattern,
                         {'code': IntSchema('code'), 'detail': StringSchema('详情'), 'data': data},
                         additional_properties, required, items, default, read_only, **extra)


class WhetherDetailSchema(Schema):

    def __init__(self, whether: str, description=None, title=None, format=None, enum=None, pattern=None,
                 additional_properties=None, required=None, items=None,
                 default=None, read_only=None, **extra):
        super().__init__(title, description, TYPE_OBJECT, format, enum, pattern,
                         {'whether': IntSchema(whether), 'detail': StringSchema('详情')},
                         additional_properties, required, items, default, read_only, **extra)
