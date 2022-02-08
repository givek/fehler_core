from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone

from fehler_auth.models import User

from .serializers import (
    ProjectSerializer,
)
from .models import Project, ProjectMembership
from spaces.models import Space


class ListProjects(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, space_name):
        """
        Return a list of all projects a particular user is associated with.
        """
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


class AddProjectMember(APIView):
    permission_classes = [IsAuthenticated]

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


class CreateProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new project with provided credentials.
        """
        project_serializer = ProjectSerializer(data=request.data)
        if project_serializer.is_valid(raise_exception=True):
            new_project = project_serializer.save()
            if new_project:
                owner_email = request.data["owner"]
                owner = User.objects.get(email=owner_email)
                user = self.create_project_membership(owner, new_project.id)
                project_memberships = ProjectMembership.objects.filter(user=owner)
                user_projects = [
                    {
                        "id": project_membership.project_id,
                        "name": project_membership.project.name,
                        "space": project_membership.project.space.name,
                    }
                    for project_membership in project_memberships
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
