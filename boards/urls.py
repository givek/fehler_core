from django.urls import path


from .views import (
    # ListTasks,
    # CreateTask,
    # DeleteTask,
    ReorderTasks,
    Tasks,
    # UpdateTask,
    AssignTask,
    CreateBoard,
    Columns,
)

urlpatterns = [
    # path(
    #     "spaces/<str:space_name>/projects/<str:project_name>/risks/",
    #     Risks.as_view(),
    #     name="list_risks",
    # ),
    # path(
    #     "spaces/<str:space_name>/projects/<str:project_name>/risks/<int:risk_id>/",
    #     Risks.as_view(),
    #     name="list_risks",
    # ),
    path(
        "spaces/<str:space_name>/projects/<str:project_name>/boards/<int:board_id>/tasks/",
        Tasks.as_view(),
        name="list_tasks",
    ),
    path(
        "spaces/<str:space_name>/projects/<str:project_name>/boards/<int:board_id>/tasks/<int:task_id>/",
        Tasks.as_view(),
        name="list_risks",
    ),
    # path(
    #     "<str:space_name>/<str:project_name>/create_task/",
    #     CreateTask.as_view(),
    #     name="create_task",
    # ),
    # path("delete_task/<int:task_id>/", DeleteTask.as_view(), name="delete_task"),
    # path("update_task/<int:task_id>/", UpdateTask.as_view(), name="update_task"),
    
    # url not used.
    path(
        # "assign_task/<str:space_name>/<str:project_name>/<int:task_id>/",
        "spaces/<str:space_name>/projects/<str:project_name>/tasks/<int:task_id>/assign/",
        AssignTask.as_view(),
        name="assign_task",
    ),
    path("create-board/", CreateBoard.as_view(), name="create_board"),
    path(
        "<str:space_name>/<str:project_name>/columns/",
        Columns.as_view(),
        name="columns",
    ),
    path("reorder-tasks/", ReorderTasks.as_view(), name="reorder-tasks"),
    # path(
    #     "reorder-column-tasks/", ReorderTaskColumns.as_view(), name="reorder-col-tasks"
    # ),
]
