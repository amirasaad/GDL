from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from gdrive.drive.models import GFile


class TestGFileModel(TestCase):
    def test_gfile_str(self):
        file_name = "txt.pdf"
        gfile = GFile.objects.create(
            file=SimpleUploadedFile(file_name, b"some content")
        )
        assert str(gfile) == file_name

    def test_gfile_title(self):
        file_name = "txt.pdf"
        gfile = GFile.objects.create(
            file=SimpleUploadedFile(file_name, b"some content")
        )
        assert gfile.title == file_name

    def test_gfile_get_absloute_url(self):
        file_name = "txt.pdf"
        gfile = GFile.objects.create(
            file=SimpleUploadedFile(file_name, b"some content")
        )
        assert gfile.get_absolute_url() == f"/drive/files/{gfile.pk}/"
