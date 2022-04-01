from django.urls import path


from .views import (
    CreateProject,
    ListProjects,
    DeleteProject,
    ProjectInfo,
    ProjectTasks,
    UpdateProject,
    AddProjectMember,
)

urlpatterns = [
    path("<str:space_name>/projects/", ListProjects.as_view(), name="list_projects"),
    path(
        "<str:space_name>/create-project/",
        CreateProject.as_view(),
        name="create_project",
    ),
    path(
        "delete_project/<int:project_id>/",
        DeleteProject.as_view(),
        name="delete_project",
    ),
    path(
        "update_project/<int:project_id>/",
        UpdateProject.as_view(),
        name="update_project",
    ),
    path(
        "add_project_member/<str:space_name>/<str:project_name>/",
        AddProjectMember.as_view(),
        name="add_project_member",
    ),
    path(
        "<str:space_name>/<str:project_name>/info/",
        ProjectInfo.as_view(),
        name="add_project_member",
    ),
    path(
        "<str:space_name>/<str:project_name>/user_tasks/",
        ProjectTasks.as_view(),
        name="user_tasks",
    ),
]
