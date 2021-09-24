import typing

from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class ImageFileStorage(fields.Field):
    default_error_messages = {
        'invalid': 'invalid file'
    }

    def _deserialize(
            self,
            value: typing.Any,
            attr: typing.Optional[str],
            data: typing.Optional[typing.Mapping[str, typing.Any]],
            **kwargs
    ):
        if not isinstance(value, FileStorage):
            return self.fail('invalid')
        if value is None:
            return None
        return value


class ImageSchema(Schema):
    image = ImageFileStorage(required=True)
