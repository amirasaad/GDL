from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from model_utils.models import TimeStampedModel

User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if instance.user is None:
        return f"files/{instance.id}/{filename}"
    return f"files/users/{instance.user.id}/files/{instance.id}/{filename}"


class GFile(TimeStampedModel):
    """
    GFile model store all files uploaded by user or anon
    """

    user = models.ForeignKey(
        User, related_name="files", null=True, on_delete=models.SET_NULL
    )
    file = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "ppt", "pptx"])],
    )

    class Meta:
        ordering = ["-created"]
