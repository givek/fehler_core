from django.urls import path

from .views import (
    # CreateSpace,
    # ListSpaces,
    # DeleteSpace,
    SpaceMembers,
    SpaceTasks,
    Spaces,
)


urlpatterns = [
    # path("spaces/", ListSpaces.as_view(), name="list_spaces"),
    # path("create-space/", CreateSpace.as_view(), name="create_space"),
    # path("delete_space/<int:space_id>", DeleteSpace.as_view(), name="delete_space"),
    # URL to handle requests without indentifiers. eg: Spaces: GET and POST
    path("spaces/", Spaces.as_view(), name="spaces"),
    # url to handle request with indentifiers. eg: Spaces: DELETE
    path("spaces/<int:space_id>/", Spaces.as_view(), name="spaces"),
    path(
        # "<str:space_name>/space-members/",
        "spaces/<str:space_name>/members/",
        SpaceMembers.as_view(),
        name="project_members",
    ),
    path(
        "spaces/<str:space_name>/tasks/",
        SpaceTasks.as_view(),
        name="user_tasks",
    ),
]
