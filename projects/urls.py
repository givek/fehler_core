from django.urls import path

from .views import CreateProject, ListProjects

urlpatterns = [
    path("projects/<int:user_id>", ListProjects.as_view(), name="list_projects"),
    path("create_project", CreateProject.as_view(), name="create_project"),
]