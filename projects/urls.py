from django.urls import path

from .views import (
    CreateProject,
    ListProjects,
    DeleteProject,
    ListTasks,
    UpdateProject,
    CreateTask,
    DeleteTask,
    UpdateTask,
    AddProjectMember,
    AssignTask,
)

urlpatterns = [
    path("<str:space_name>/projects/", ListProjects.as_view(), name="list_projects"),
    path("create-project/", CreateProject.as_view(), name="create_project"),
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
    path("tasks/", ListTasks.as_view(), name="list_tasks"),
    path("create_task/", CreateTask.as_view(), name="create_task"),
    path("delete_task/<int:task_id>/", DeleteTask.as_view(), name="delete_task"),
    path("update_task/<int:task_id>/", UpdateTask.as_view(), name="update_task"),
    path(
        "add_project_member/<str:space_name>/<str:project_name>/",
        AddProjectMember.as_view(),
        name="add_project_member",
    ),
    path(
        "assign_task/<str:space_name>/<str:project_name>/<int:task_id>/",
        AssignTask.as_view(),
        name="assign_task",
    ),
]
