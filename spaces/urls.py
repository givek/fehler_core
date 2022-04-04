from django.urls import path

from .views import CreateSpace, ListSpaces, DeleteSpace, SpaceMembers


urlpatterns = [
    path("spaces/", ListSpaces.as_view(), name="list_spaces"),
    path("create-space/", CreateSpace.as_view(), name="create_space"),
    path("delete_space/<int:space_id>", DeleteSpace.as_view(), name="delete_space"),
    path(
        "<str:space_name>/space-members/",
        SpaceMembers.as_view(),
        name="project_members",
    ),
]
