from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from gdrive.drive.api.views import GFileViewSet
from gdrive.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("files", GFileViewSet, basename="file")


app_name = "api"
urlpatterns = router.urls
