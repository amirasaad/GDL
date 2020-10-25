from rest_framework import serializers

from gdrive.drive.models import GFile


class GFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFile
        fields = ["id", "file", "created"]
