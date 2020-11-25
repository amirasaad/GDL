from typing import List

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from model_utils.models import TimeStampedModel

from gdrive.utils.validators import FileContentTypeValidator

User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if instance.folder is None:
        return f"{filename}"
    return f"{instance.folder.get_sub_folder_path()}{filename}"


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
            FileExtensionValidator(allowed_extensions=["pdf", "ppt", "pptx"]),
            FileContentTypeValidator(
                allowed_content_types=[
                    "application/pdf",
                    "application/vnd.ms-powerpoint",
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                ]
            ),
        ],
    )
    folder = models.ForeignKey(
        "GFolder", related_name="files", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-created"]

    @cached_property
    def title(self):
        return self.file.name.split("/").pop()

    def get_absolute_url(self):
        return reverse("drive:file-detail", kwargs={"pk": self.pk})

    def get_path(self):
        if self.folder is None:
            return f"/{self.title}"
        return self.folder.get_sub_folder_path() + self.title

    def __str__(self):
        return self.title


class GFolder(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name="folders", null=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(
        "GFolder", related_name="folders", null=True, on_delete=models.SET_NULL
    )

    def get_sub_folder_path(self):
        """
        Return path of sub all folders
        """
        base = f"{self.name}/"
        parent = self.folder
        dirs: List[str] = []
        while parent is not None:
            dirs.insert(0, f"{parent.name}/")
            parent = parent.folder
        return "".join(dirs) + base
