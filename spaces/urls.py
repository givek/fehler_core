from django.urls import path

from .views import CreateSpace, ListSpaces


urlpatterns = [
    path("spaces/", ListSpaces.as_view(), name="list_spaces"),
    path("create-space/", CreateSpace.as_view(), name="create_space"),
]
