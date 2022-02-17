from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from fehler_auth.models import User

from .serializers import (
    TaskSerializer,
    BoardSerializer,
    ColumnSerializer,
    LabelSerializer,
)
from .models import Task, Board, Column, Label
from spaces.models import Space
from projects.models import Project


class CreateBoard(APIView):
    def post(self, request):
        """
        Create a new board with provided credentials.
        """
        board_serializer = BoardSerializer(data=request.data)
        if board_serializer.is_valid(raise_exception=True):
            new_board = board_serializer.save()
            if new_board:
                boards = Board.objects.all()
                board_serializer = BoardSerializer(boards, many=True)
                return Response(board_serializer.data, status=status.HTTP_200_OK)
        return Response(board_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTasks(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, space_name, project_name, board_id):
        """
        Return a list of all tasks associated with a particular project.
        """

        # TODO: search project inside a space.
        # board = Board.objects.get(id=board_id)

        tasks = Task.objects.filter(column__board=board_id)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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


class AssignTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id, space_name, project_name):
        """
        Assign a task to a user.
        """
        space = Space.objects.get(name=space_name)
        project = Project.objects.get(name=project_name, space__name=space_name)
        task = Task.objects.get(id=task_id)
        user = User.objects.get(email=request.data["email"])
        if user in task.project.get_members():
            task.assignee = user
            task.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
