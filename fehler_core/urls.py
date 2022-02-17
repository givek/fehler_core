from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("fehler_auth.urls")),
    path("api/", include("spaces.urls")),
    path("api/", include("projects.urls")),
    path("api/", include("boards.urls")),
]
