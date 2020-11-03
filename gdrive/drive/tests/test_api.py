from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from gdrive.drive.models import GFile, GFolder


class TestUploadFile(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/files/"

    def test_user_retrieve_all_files(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

    def test_user_can_upload_file(self):
        pdf = BytesIO(
            b"%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1"
            b">>endobj 3 0 obj<</Type/Page/MediaBox[0 0 3 3]>>endobj\nxref\n0 4\n0000000000 65535 f\n000000"
            b"0010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxre"
            b"f\n149\n%EOF\n"
        )
        simple_file = SimpleUploadedFile(
            "txt.pdf", pdf.read(), content_type="application/pdf"
        )
        data = {"file": simple_file}
        resp = self.client.post(self.url, data)
        print(resp.data)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_user_can_not_upload_file_wrong_ext_right_content_type(self):
        simple_file = SimpleUploadedFile(
            "txt.txt", b"some content", content_type="application/pdf"
        )
        data = {"file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        self.assertIn("File extension “txt” is not allowed.", str(resp.data["file"]))

    def test_user_can_not_upload_document_is_not_pdf_or_pptx(self):
        simple_file = SimpleUploadedFile("txt.txt", b"some content")

        data = {"name": "test", "file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        self.assertIn("File extension “txt” is not allowed.", str(resp.data["file"]))

    def test_retrieve_name_from_file_path(self):
        file_name = "txt.pdf"
        doc = GFile.objects.create(
            file=SimpleUploadedFile(
                file_name, b"some content", content_type="application/pdf"
            )
        )
        resp = self.client.get(f"{self.url}{doc.id}/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["name"] == file_name

    def test_user_can_not_upload_empty_file(self):
        simple_file = SimpleUploadedFile("txt.pdf", b"", content_type="application/pdf")
        data = {"file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        self.assertIn("The submitted file is empty.", str(resp.data["file"]))

    def test_user_can_upload_file_within_folder(self):
        simple_file = SimpleUploadedFile(
            "txt.pdf", b"some content", content_type="application/pdf"
        )
        folder = GFolder.objects.create(name="newfiledir")
        data = {"file": simple_file, "folder": folder.id}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        file = GFile.objects.get(pk=resp.data["id"])
        assert file.folder == folder


class TestFolder(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/folders/"

    def test_create_empty_folder(self):
        data = {"name": "directory1"}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert GFolder.objects.all().count() == 1

    def test_add_file_to_folder(self):
        file_name = "txt.pdf"
        doc = GFile.objects.create(file=SimpleUploadedFile(file_name, b"some content"))
        folder = GFolder.objects.create(name="directory2")
        resp = self.client.post(f"{self.url}{folder.id}/add_file/", {"file": doc.id})
        assert resp.status_code == status.HTTP_201_CREATED
        doc.refresh_from_db()
        assert doc.folder == folder

    def test_add_folder_to_another_folder(self):
        folder1 = GFolder.objects.create(name="directory3")
        folder2 = GFolder.objects.create(name="directory3")
        resp = self.client.post(
            f"{self.url}{folder1.id}/add_folder/", {"folder": folder2.id}
        )
        assert resp.status_code == status.HTTP_201_CREATED
        folder1.refresh_from_db()
        assert folder1.folder == folder2
