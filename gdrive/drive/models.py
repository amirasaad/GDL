from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from model_utils.models import TimeStampedModel

from gdrive.utils.validators import FileContentTypeValidator

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
        validators=[
            FileContentTypeValidator(
                allowed_content_types=[
                    "application/pdf",
                    "application/vnd.ms-powerpoint",
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                ]
            )
        ],
    )

    class Meta:
        ordering = ["-created"]

    @cached_property
    def title(self):
        return self.file.name.split("/").pop()

    def get_absolute_url(self):
        return reverse("drive:file-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
