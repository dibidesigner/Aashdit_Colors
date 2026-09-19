from django.urls import path
from .views import PopularSectorListView, SectorSaveView


urlpatterns = [
    path(
        "",
        SectorSaveView.as_view(),
        name="sector-root-save",
    ),
    path(
        "save/",
        SectorSaveView.as_view(),
        name="sector-save",
    ),
    path(
        "save/<int:pk>/",
        SectorSaveView.as_view(),
        name="sector-save-detail",
    ),
    path(
        "popular-sectors/",
        PopularSectorListView.as_view(),
        name="popular-sectors",
    ),
    path(
        "popular-sector-save/",
        PopularSectorListView.as_view(),
        name="popular-sector-save",
    ),
]