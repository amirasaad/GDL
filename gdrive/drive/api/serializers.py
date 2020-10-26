from rest_framework import serializers

from gdrive.drive.models import GFile


class GFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = GFile
        fields = ["id", "file", "created", "name"]

    def get_name(self, obj):
        path = obj.file.name.split("/")
        return path.pop()
