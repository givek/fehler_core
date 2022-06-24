from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone

from fehler_auth.models import User
from fehler_auth.serializers import UserSerializer

from .serializers import (
    ProjectSerializer,
    RiskSerializer,
)
from .models import Project, ProjectMembership, Risk
from spaces.models import Space
from boards.models import Board, Column, Task
from boards.serializers import TaskSerializer


class Projects(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request, space_name):
    #     """
    #     Return a list of all projects a particular user is associated with.
    #     """
    #     project_memberships = ProjectMembership.objects.filter(user=request.user.id)
    #     # only return projects from that particular space.
    #     user_projects = [
    #         {
    #             "id": project_membership.project_id,
    #             "name": project_membership.project.name,
    #             "space": project_membership.project.space.name,
    #         }
    #         for project_membership in project_memberships
    #         if project_membership.project.space.name == space_name
    #     ]
    #     return Response(user_projects, status=status.HTTP_200_OK)

    def get(self, request, space_name, project_name=None):
        """
        Return a project from a particular space with a user is associated with.
        """

        if not project_name:
            project_memberships = ProjectMembership.objects.filter(user=request.user.id)
            # only return projects from that particular space.
            user_projects = [
                {
                    "id": project_membership.project_id,
                    "name": project_membership.project.name,
                    "space": project_membership.project.space.name,
                }
                for project_membership in project_memberships
                if project_membership.project.space.name == space_name
            ]
            return Response(user_projects, status=status.HTTP_200_OK)

        space = Space.objects.get(name=space_name)

        project = Project.objects.filter(space=space).get(name=project_name)

        return Response(
            {"id": project.id, "name": project.name, "space": space.name},
            status=status.HTTP_200_OK,
        )

    def post(self, request, space_name):
        """
        Create a new project with provided credentials.
        """
        # name, space, description, (request.user)

        # for now, use request.user
        # TODO: lead

        print("data", request.data)
        print("user", request.user)

        space = Space.objects.get(name=space_name)

        project_serializer = ProjectSerializer(
            data={"name": request.data["name"], "space": space.id}
        )

        if project_serializer.is_valid(raise_exception=True):
            new_project = project_serializer.save()
            if new_project:
                new_project_membership = self.create_project_membership(
                    request.user, new_project.id
                )
                project_memberships = ProjectMembership.objects.filter(
                    user=request.user
                )

                project_board = Board.objects.create(
                    name=f"{new_project.name}-board", project=new_project
                )

                Column.objects.create(
                    title="Backlog", board=project_board, column_order=1
                )
                Column.objects.create(
                    title="Doing", board=project_board, column_order=2
                )
                Column.objects.create(title="Done", board=project_board, column_order=3)

                user_projects = [
                    {
                        "id": project_membership.project_id,
                        "name": project_membership.project.name,
                        "space": project_membership.project.space.name,
                    }
                    for project_membership in project_memberships
                    if project_membership.project.space.name == space_name
                ]
                return Response(user_projects, status=status.HTTP_200_OK)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_project_membership(self, user, project_id):
        project = Project.objects.get(id=project_id)
        user = ProjectMembership.objects.create(user=user, project=project)
        user.save()

    def put(self, request, space_name, project_name):
        """
        Update a project with provided credentials.
        """
        space = Space.objects.get(name=space_name)
        space_projects = Project.objects.filter(space=space)
        project = space_projects.get(name=project_name)
        project_serializer = ProjectSerializer(project, data=request.data)
        if project_serializer.is_valid(raise_exception=True):
            project_serializer.save()
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, space_name, project_name):
        """
        Delete a project with provided credentials.
        """
        space = Space.objects.get(name=space_name)
        space_projects = Project.objects.filter(space=space)
        project = space_projects.get(name=project_name)
        # project = Project.objects.get(id=project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProjectInfo(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, space_name, project_name):
#         """
#         Return a list of all projects a particular user is associated with.
#         """

#         space = Space.objects.get(name=space_name)

#         project = Project.objects.filter(space=space).get(name=project_name)

#         return Response(
#             {"id": project.id, "name": project.name, "space": space.name},
#             status=status.HTTP_200_OK,
#         )


# class ListProjects(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, space_name):
#         """
#         Return a list of all projects a particular user is associated with.
#         """
#         project_memberships = ProjectMembership.objects.filter(user=request.user.id)
#         # only return projects from that particular space.
#         user_projects = [
#             {
#                 "id": project_membership.project_id,
#                 "name": project_membership.project.name,
#                 "space": project_membership.project.space.name,
#             }
#             for project_membership in project_memberships
#             if project_membership.project.space.name == space_name
#         ]
#         return Response(user_projects, status=status.HTTP_200_OK)


class ProjectMember(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, space_name, project_name):
        """
        Return a list of all tasks associated with a particular space of a particular user.
        """
        project = get_object_or_404(Project, name=project_name)
        project_members = project.get_members()
        print("proejct meber", project_members)
        serializer = UserSerializer(project_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, space_name, project_name):
        """
        Add a user to a project.
        """
        space = Space.objects.get(name=space_name)
        user = User.objects.get(email=request.data["email"])
        if user in space.get_members():
            project = Project.objects.get(name=project_name, space__name=space_name)

            project_membership = ProjectMembership(
                project=project, user=user, date_joined=timezone.now()
            )
            project_membership.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class AddProjectMember(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, space_name, project_name):
#         """
#         Add a user to a project.
#         """
#         space = Space.objects.get(name=space_name)
#         user = User.objects.get(email=request.data["email"])
#         if user in space.get_members():
#             project = Project.objects.get(name=project_name, space__name=space_name)

#             project_membership = ProjectMembership(
#                 project=project, user=user, date_joined=timezone.now()
#             )
#             project_membership.save()
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# class ProjectMembers(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, space_name, project_name):
#         """
#         Return a list of all tasks associated with a particular space of a particular user.
#         """
#         project = get_object_or_404(Project, name=project_name)
#         project_members = project.get_members()
#         print("proejct meber", project_members)
#         serializer = UserSerializer(project_members, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CreateProject(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         """
#         Create a new project with provided credentials.
#         """
#         project_serializer = ProjectSerializer(data=request.data)
#         if project_serializer.is_valid(raise_exception=True):
#             new_project = project_serializer.save()
#             if new_project:
#                 owner_email = request.data["owner"]
#                 owner = User.objects.get(email=owner_email)
#                 user = self.create_project_membership(owner, new_project.id)
#                 project_memberships = ProjectMembership.objects.filter(user=owner)
#                 user_projects = [
#                     {
#                         "id": project_membership.project_id,
#                         "name": project_membership.project.name,
#                         "space": project_membership.project.space.name,
#                     }
#                     for project_membership in project_memberships
#                 ]
#                 return Response(user_projects, status=status.HTTP_200_OK)
#         return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def create_project_membership(self, user, project_id):
#         project = Project.objects.get(id=project_id)
#         user = ProjectMembership.objects.create(user=user, project=project)
#         user.save()


class CreateProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, space_name):
        """
        Create a new project with provided credentials.
        """
        # name, space, description, (request.user)

        # for now, use request.user
        # TODO: lead

        print("data", request.data)
        print("user", request.user)

        space = Space.objects.get(name=space_name)

        project_serializer = ProjectSerializer(
            data={"name": request.data["name"], "space": space.id}
        )

        if project_serializer.is_valid(raise_exception=True):
            new_project = project_serializer.save()
            if new_project:
                new_project_membership = self.create_project_membership(
                    request.user, new_project.id
                )
                project_memberships = ProjectMembership.objects.filter(
                    user=request.user
                )

                project_board = Board.objects.create(
                    name=f"{new_project.name}-board", project=new_project
                )

                Column.objects.create(
                    title="Backlog", board=project_board, column_order=1
                )
                Column.objects.create(
                    title="Doing", board=project_board, column_order=2
                )
                Column.objects.create(title="Done", board=project_board, column_order=3)

                user_projects = [
                    {
                        "id": project_membership.project_id,
                        "name": project_membership.project.name,
                        "space": project_membership.project.space.name,
                    }
                    for project_membership in project_memberships
                    if project_membership.project.space.name == space_name
                ]
                return Response(user_projects, status=status.HTTP_200_OK)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_project_membership(self, user, project_id):
        project = Project.objects.get(id=project_id)
        user = ProjectMembership.objects.create(user=user, project=project)
        user.save()


class DeleteProject(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id):
        """
        Delete a project with provided credentials.
        """
        project = Project.objects.get(id=project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateProject(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id):
        """
        Update a project with provided credentials.
        """
        project = Project.objects.get(id=project_id)
        project_serializer = ProjectSerializer(project, data=request.data)
        if project_serializer.is_valid(raise_exception=True):
            project_serializer.save()
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectTasks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, space_name, project_name):
        """
        Return a list of all tasks associated with a particular space of a particular user.
        """

        space = Space.objects.get(name=space_name)
        project = Project.objects.filter(space=space).get(name=project_name)
        tasks = Task.objects.filter(project=project).filter(assignee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Risks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, space_name, project_name):
        """
        Return a list of all tasks associated with a particular project.
        """
        space = Space.objects.get(name=space_name)
        project = Project.objects.filter(space=space).get(name=project_name)
        risks = Risk.objects.filter(project=project.id)
        serializer = RiskSerializer(risks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, space_name, project_name):
        """
        Create a new risk with provided credentials.
        """
        risk_serializer = RiskSerializer(data=request.data)
        if risk_serializer.is_valid(raise_exception=True):
            new_risk = risk_serializer.save()
            # risk_serializer.save()

            if new_risk:
                project = Project.objects.get(name=project_name)
                risks = Risk.objects.filter(project=project)
                serializer = RiskSerializer(risks, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(risk_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, space_name, project_name, risk_id):
        """
        Update a risk with provided credentials.
        """
        risk = Risk.objects.get(id=risk_id)
        risk_serializer = RiskSerializer(risk, data=request.data)
        if risk_serializer.is_valid(raise_exception=True):
            risk_serializer.save()
            return Response(risk_serializer.data, status=status.HTTP_200_OK)
        return Response(risk_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, space_name, project_name, risk_id):
        """
        Delete a risk with provided credentials.
        """
        risk = Risk.objects.get(id=risk_id)
        risk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ListRisks(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, space_name, project_name):
#         """
#         Return a list of all tasks associated with a particular project.
#         """
#         project = Project.objects.get(name=project_name)
#         risks = Risk.objects.filter(project=project.id)
#         serializer = RiskSerializer(risks, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CreateRisk(APIView):
#     def post(self, request, space_name, project_name):
#         """
#         Create a new risk with provided credentials.
#         """
#         risk_serializer = RiskSerializer(data=request.data)
#         if risk_serializer.is_valid(raise_exception=True):
#             new_risk = risk_serializer.save()
#             # risk_serializer.save()

#             if new_risk:
#                 project = Project.objects.get(name=project_name)
#                 risks = Risk.objects.filter(project=project)
#                 serializer = RiskSerializer(risks, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(risk_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdateRisk(APIView):
#     def put(self, request, risk_id):
#         """
#         Update a risk with provided credentials.
#         """
#         risk = Risk.objects.get(id=risk_id)
#         risk_serializer = RiskSerializer(risk, data=request.data)
#         if risk_serializer.is_valid(raise_exception=True):
#             risk_serializer.save()
#             return Response(risk_serializer.data, status=status.HTTP_200_OK)
#         return Response(risk_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DeleteRisk(APIView):
#     def delete(self, request, risk_id):
#         """
#         Delete a risk with provided credentials.
#         """
#         risk = Risk.objects.get(id=risk_id)
#         risk.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
