from django.urls import path


from .views import (
    ListTasks,
    CreateTask,
    DeleteTask,
    ReorderTasks,
    UpdateTask,
    AssignTask,
    CreateBoard,
    Columns,
)

urlpatterns = [
    path(
        "<str:space_name>/<str:project_name>/create_task/",
        CreateTask.as_view(),
        name="create_task",
    ),
    path("delete_task/<int:task_id>/", DeleteTask.as_view(), name="delete_task"),
    path("update_task/<int:task_id>/", UpdateTask.as_view(), name="update_task"),
    path(
        "assign_task/<str:space_name>/<str:project_name>/<int:task_id>/",
        AssignTask.as_view(),
        name="assign_task",
    ),
    path("create-board/", CreateBoard.as_view(), name="create_board"),
    path(
        "<str:space_name>/<str:project_name>/columns/",
        Columns.as_view(),
        name="columns",
    ),
    path(
        "<str:space_name>/<str:project_name>/<int:board_id>/tasks/",
        ListTasks.as_view(),
        name="list_tasks",
    ),
    path("reorder-tasks/", ReorderTasks.as_view(), name="reorder-tasks"),
    # path(
    #     "reorder-column-tasks/", ReorderTaskColumns.as_view(), name="reorder-col-tasks"
    # ),
]
