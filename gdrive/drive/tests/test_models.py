from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from gdrive.drive.models import GFile, GFolder


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

    def test_gfile_get_full_folders_path(self):

        dir1 = GFolder.objects.create(name="dir1")
        dir2 = GFolder.objects.create(name="dir2", folder=dir1)
        dir3 = GFolder.objects.create(name="dir3", folder=dir2)
        file_name = "test.pdf"
        gfile = GFile.objects.create(
            file=SimpleUploadedFile(file_name, b"some content"), folder=dir3
        )
        assert gfile.get_path() == "dir1/dir2/dir3/test.pdf"


class TestGFolder(TestCase):
    def test_get_sub_folders(self):
        dir1 = GFolder.objects.create(name="dir1")
        dir2 = GFolder.objects.create(name="dir2", folder=dir1)
        dir3 = GFolder.objects.create(name="dir3", folder=dir2)
        assert dir1.get_sub_folder_path() == "dir1/"
        assert dir2.get_sub_folder_path() == "dir1/dir2/"
        assert dir3.get_sub_folder_path() == "dir1/dir2/dir3/"
