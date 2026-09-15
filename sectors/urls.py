from django.contrib import admin
from django.urls import path, include
from .views import PopularSectorListView


urlpatterns = [
    path(
        "popular-sectors/",
        PopularSectorListView.as_view(),
        name="popular-sectors",
    ),
    path(
    "popular-sector-save/",
    PopularSectorListView.as_view(),
    name="sector-list-create"
)
]