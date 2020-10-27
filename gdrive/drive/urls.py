from django.urls import path

from .views import GfileDetailView

app_name = "drive"

urlpatterns = [
    path("files/<int:pk>/", view=GfileDetailView.as_view(), name="file-detail"),
]
