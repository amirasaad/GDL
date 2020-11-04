import magic
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileContentTypeValidator:
    message = _(
        "File content type “%(content_type)s” is not allowed. "
        "Allowed content types are: %(allowed_content_types)s."
    )
    code = "invalid_content_type"

    def __init__(self, allowed_content_types=None, message=None, code=None):
        if allowed_content_types is not None:
            allowed_content_types = [
                allowed_content_type.lower()
                for allowed_content_type in allowed_content_types
            ]
        self.allowed_content_types = allowed_content_types
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        content_type = magic.from_buffer(value.read(1024), mime=True)
        if (
            self.allowed_content_types is not None
            and content_type not in self.allowed_content_types
        ):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "content_type": content_type,
                    "allowed_content_types": ", ".join(self.allowed_content_types),
                    "value": value,
                },
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.allowed_content_types == other.allowed_content_types
            and self.message == other.message
            and self.code == other.code
        )
