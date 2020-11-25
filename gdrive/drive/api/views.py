from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gdrive.drive.models import GFile, GFolder

from .serializers import GFileSerializer, GFolderSerializer


class GFileViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = GFile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GFileSerializer
    lookup_field = "pk"

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        serializer.save()


class GFolderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = GFolder.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GFolderSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        serializer.save()

    @action(detail=True, methods=["post"])
    def add_file(self, request, *args, **kargs):
        folder = self.get_object()
        file_id = request.data["file"]
        file = get_object_or_404(GFile, pk=file_id)
        file.folder = folder
        file.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def add_folder(self, request, *args, **kargs):
        folder = self.get_object()
        folder_id = request.data["folder"]
        folder_ = get_object_or_404(GFolder, pk=folder_id)
        folder.folder = folder_
        folder.save()
        return Response(status=status.HTTP_201_CREATED)
