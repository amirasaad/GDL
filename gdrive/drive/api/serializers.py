from rest_framework import serializers

from gdrive.drive.models import GFile, GFolder


class GFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.CharField(source="get_absolute_url", read_only=True)

    class Meta:
        model = GFile
        fields = ["id", "file", "created", "name", "url", "folder"]

    def get_name(self, obj):
        path = obj.file.name.split("/")
        return path.pop()


class GFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFolder
        fields = ["id", "created", "name"]
