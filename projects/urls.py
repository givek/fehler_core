from django.urls import path


from .views import (
    # CreateProject,
    # CreateRisk,
    # DeleteRisk,
    # ListProjects,
    # DeleteProject,
    # ListRisks,
    # ProjectInfo,
    ProjectMember,
    # ProjectMembers,
    ProjectTasks,
    Projects,
    # UpdateProject,
    # AddProjectMember,
    # UpdateRisk,
    Risks,
)

urlpatterns = [
    path("spaces/<str:space_name>/projects/", Projects.as_view(), name="projects"),
    path(
        "spaces/<str:space_name>/projects/<str:project_name>/",
        Projects.as_view(),
        name="projects",
    ),
    # path(
    #     "<str:space_name>/create-project/",
    #     CreateProject.as_view(),
    #     name="create_project",
    # ),
    # path(
    #     "delete_project/<int:project_id>/",
    #     DeleteProject.as_view(),
    #     name="delete_project",
    # ),
    # path(
    #     "update_project/<int:project_id>/",
    #     UpdateProject.as_view(),
    #     name="update_project",
    # ),
    path(
        "spaces/<str:space_name>/projects/<str:project_name>/members/",
        ProjectMember.as_view(),
        name="projects",
    ),
    # path(
    #     "add_project_member/<str:space_name>/<str:project_name>/",
    #     AddProjectMember.as_view(),
    #     name="add_project_member",
    # ),
    # path(
    #     "<str:space_name>/<str:project_name>/project-members/",
    #     ProjectMembers.as_view(),
    #     name="project_members",
    # ),
    # path(
    #     "<str:space_name>/<str:project_name>/info/",
    #     ProjectInfo.as_view(),
    #     name="project_info",
    # ),
    path(
        "<str:space_name>/<str:project_name>/user_tasks/",
        ProjectTasks.as_view(),
        name="user_tasks",
    ),
    # path(
    #     "<str:space_name>/<str:project_name>/project-members/",
    #     ProjectMembers.as_view(),
    #     name="project_members",
    # ),
    # path(
    #     "<str:space_name>/<str:project_name>/risks/",
    #     ListRisks.as_view(),
    #     name="list_risks",
    # ),
    # path(
    #     "<str:space_name>/<str:project_name>/create-risk/",
    #     CreateRisk.as_view(),
    #     name="create_risk",
    # ),
    # path("<int:risk_id>/update-risk/", UpdateRisk.as_view(), name="update_risk"),
    # path("<int:risk_id>/delete-risk/", DeleteRisk.as_view(), name="delete_risk"),
    path(
        "spaces/<str:space_name>/projects/<str:project_name>/risks/",
        Risks.as_view(),
        name="list_risks",
    ),
    path(
        "spaces/<str:space_name>/projects/<str:project_name>/risks/<int:risk_id>/",
        Risks.as_view(),
        name="list_risks",
    ),
]
