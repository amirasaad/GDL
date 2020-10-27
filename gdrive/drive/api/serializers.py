from rest_framework import serializers

from gdrive.drive.models import GFile


class GFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.CharField(source="get_absolute_url", read_only=True)

    class Meta:
        model = GFile
        fields = ["id", "file", "created", "name", "url"]

    def get_name(self, obj):
        path = obj.file.name.split("/")
        return path.pop()
