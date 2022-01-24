from django.urls import path

from .views import CreateProject, ListProjects, ListTasks, CreateTask

urlpatterns = [
    path("projects/<int:user_id>", ListProjects.as_view(), name="list_projects"),
    path("create_project", CreateProject.as_view(), name="create_project"),
    path("tasks", ListTasks.as_view(), name="list_tasks"),
    path("create_task", CreateTask.as_view(), name="create_task"),
]
