from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(
        "api/auth/",
        include("accounts.urls")
    ),
    path(
        "api/sectors/",
        include("sectors.urls")
    ),
    path(
        "",
        admin.site.urls
    ),
]