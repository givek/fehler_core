from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from fehler_auth.models import User

from .serializers import ProjectSerializer
from .models import ProjectMembership
from .models import Project


class ListProjects(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """
        Return a list of all projects a particular user is associated with.
        """
        project_memberships = ProjectMembership.objects.filter(user=user_id)
        user_projects = [
                    {
                        "id": project_membership.project_id,
                        "name": project_membership.project.name,
                        "space": project_membership.project.space.name,
                    }
                    for project_membership in project_memberships
                ]
        return Response(user_projects, status=status.HTTP_200_OK)

class CreateProject(APIView):
    permission_classes = [AllowAny]

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
        user = ProjectMembership.objects.create(
            user=user, project=project
        )
        user.save()