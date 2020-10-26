from django.urls import path

from .views import PeriodicalSearchView

urlpatterns = [
    path(
        "search/",
        PeriodicalSearchView(template="search/search.html"),
        name="haystack_search",
    ),
]
