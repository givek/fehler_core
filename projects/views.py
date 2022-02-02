from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from fehler_auth.models import User

from .serializers import ProjectSerializer, TaskSerializer
from .models import Project, ProjectMembership, Task


class ListProjects(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return a list of all projects a particular user is associated with.
        """
        project_memberships = ProjectMembership.objects.filter(user=request.user.id)
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
        user = ProjectMembership.objects.create(user=user, project=project)
        user.save()


class DeleteProject(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, project_id):
        """
        Delete a project with provided credentials.
        """
        project = Project.objects.get(id=project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateProject(APIView):
    permission_classes = [AllowAny]

    def put(self, request, project_id, format=None):
        """
        Update a project with provided credentials.
        """
        project = Project.objects.get(id=project_id)
        project_serializer = ProjectSerializer(project, data=request.data)
        if project_serializer.is_valid(raise_exception=True):
            project_serializer.save()
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTasks(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return a list of all tasks associated with a particular project.
        """
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        project_tasks = [
            {
                "id": task.id,
                "name": task.name,
                "project": task.project.name,
                "type": task.type,
                "description": task.description,
                "assignee": task.assignee.email if task.assignee else None,
                "labels": task.labels,
                "reporter": task.reporter.email if task.reporter else None,
                "status": task.status,
            }
            for task in tasks
        ]
        return Response(project_tasks, status=status.HTTP_200_OK)


class CreateTask(APIView):
    def post(self, request):
        """
        Create a new task with provided credentials.
        """
        task_serializer = TaskSerializer(data=request.data)
        if task_serializer.is_valid(raise_exception=True):
            new_task = task_serializer.save()
            # task_serializer.save()

            if new_task:
                tasks = Task.objects.all()

                project_tasks = [
                    {
                        "id": task.id,
                        "name": task.name,
                        "project": task.project.name,
                        "type": task.type,
                        "description": task.description,
                        "assignee": task.assignee.email if task.assignee else None,
                        "labels": task.labels,
                        "reporter": task.reporter.email if task.reporter else None,
                        "status": task.status,
                    }
                    for task in tasks
                ]
            return Response(project_tasks, status=status.HTTP_200_OK)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTask(APIView):
    def delete(self, request, task_id):
        """
        Delete a task with provided credentials.
        """
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateTask(APIView):
    def put(self, request, task_id, format=None):
        """
        Update a task with provided credentials.
        """
        task = Task.objects.get(id=task_id)
        task_serializer = TaskSerializer(task, data=request.data)
        if task_serializer.is_valid(raise_exception=True):
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_200_OK)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
