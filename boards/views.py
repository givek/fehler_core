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


class Tasks(APIView):
    def get(self, request, space_name, project_name, board_id):
        """
        Return a list of all tasks associated with a particular project.
        """

        # TODO: search project inside a space.
        # board = Board.objects.get(id=board_id)

        tasks = Task.objects.filter(column__board=board_id)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, space_name, project_name, board_id):
        """
        Create a new task with provided credentials.
        """
        task_serializer = TaskSerializer(data=request.data)

        print(task_serializer)

        project = Project.objects.get(id=request.data["project"])

        board = Board.objects.filter(project=project).first()

        first_column = Column.objects.filter(board=board).first()

        request.data["column"] = first_column.id

        if task_serializer.is_valid(raise_exception=True):
            new_task = task_serializer.save(project=project, column=first_column)

            print("newtaskasdf")
            print("newtask", new_task)

            if new_task:
                tasks = Task.objects.all()

                # project_tasks = [
                #     {
                #         "id": task.id,
                #         "name": task.name,
                #         "project": task.project.name,
                #         "type": task.type,
                #         "description": task.description,
                #         "assignee": task.assignee.email if task.assignee else None,
                #         "labels": task.labels,
                #         "reporter": task.reporter.email if task.reporter else None,
                #         "status": task.status,
                #     }
                #     for task in tasks
                # ]

                # project_tasks = TaskSerializer(tasks, many=True)
            return Response(status=status.HTTP_200_OK)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, space_name, project_name, board_id, task_id):
        """
        Update a task with provided credentials.
        """
        task = Task.objects.get(id=task_id)

        fields_to_remove = ["assignee_name", "reporter_name", "project", "column_title"]

        for k in fields_to_remove:
            request.data.pop(k, None)

        task_serializer = TaskSerializer(task, data=request.data)
        if task_serializer.is_valid(raise_exception=True):
            print("valid")
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_200_OK)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, space_name, project_name, board_id, task_id):
        """
        Delete a task with provided credentials.
        """
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


# class ListTasks(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, space_name, project_name, board_id):
#         """
#         Return a list of all tasks associated with a particular project.
#         """

#         # TODO: search project inside a space.
#         # board = Board.objects.get(id=board_id)

#         tasks = Task.objects.filter(column__board=board_id)
#         serializer = TaskSerializer(tasks, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CreateTask(APIView):
#     def post(self, request, space_name, project_name):
#         """
#         Create a new task with provided credentials.
#         """
#         task_serializer = TaskSerializer(data=request.data)

#         print(task_serializer)

#         project = Project.objects.get(id=request.data["project"])

#         board = Board.objects.filter(project=project).first()

#         first_column = Column.objects.filter(board=board).first()

#         request.data["column"] = first_column.id

#         if task_serializer.is_valid(raise_exception=True):
#             new_task = task_serializer.save(project=project, column=first_column)

#             print("newtaskasdf")
#             print("newtask", new_task)

#             if new_task:
#                 tasks = Task.objects.all()

#                 # project_tasks = [
#                 #     {
#                 #         "id": task.id,
#                 #         "name": task.name,
#                 #         "project": task.project.name,
#                 #         "type": task.type,
#                 #         "description": task.description,
#                 #         "assignee": task.assignee.email if task.assignee else None,
#                 #         "labels": task.labels,
#                 #         "reporter": task.reporter.email if task.reporter else None,
#                 #         "status": task.status,
#                 #     }
#                 #     for task in tasks
#                 # ]

#                 # project_tasks = TaskSerializer(tasks, many=True)
#             return Response(status=status.HTTP_200_OK)
#         return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DeleteTask(APIView):
#     def delete(self, request, task_id):
#         """
#         Delete a task with provided credentials.
#         """
#         task = Task.objects.get(id=task_id)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class UpdateTask(APIView):
#     def put(self, request, task_id):
#         """
#         Update a task with provided credentials.
#         """
#         task = Task.objects.get(id=task_id)

#         fields_to_remove = ["assignee_name", "reporter_name", "project", "column_title"]

#         for k in fields_to_remove:
#             request.data.pop(k, None)

#         task_serializer = TaskSerializer(task, data=request.data)
#         if task_serializer.is_valid(raise_exception=True):
#             print("valid")
#             task_serializer.save()
#             return Response(task_serializer.data, status=status.HTTP_200_OK)
#         return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class Columns(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, space_name, project_name):
        """
        Assign a task to a user.
        """
        space = Space.objects.get(name=space_name)
        project = Project.objects.get(name=project_name, space__name=space_name)
        board = Board.objects.get(project=project)
        columns = Column.objects.filter(board=board)

        serializer = ColumnSerializer(columns, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# class Board(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, space_name, project_name):
#         """
#         Assign a task to a user.
#         """
#         space = Space.objects.get(name=space_name)
#         project = Project.objects.get(name=project_name, space__name=space_name)
#         board = Board.objects.get(project=project)
#         columns = Column.objects.filter(board=board)

#         serializer = ColumnSerializer(columns, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


from django.db.models import F


class ReorderTasks(APIView):
    def post(self, request):
        # select tasks from a particular board.

        tasks = Task.objects.filter(column__board=1)

        source_column_id = request.data["source_droppable_id"]
        destination_column_id = request.data["destination_droppable_id"]

        # add one as our order starts from 1
        source_index = request.data["source_index"] + 1
        destination_index = request.data["destination_index"] + 1

        task_id = request.data["task_id"]

        task_to_update = Task.objects.filter(id=task_id)

        if source_column_id != destination_column_id:

            print("source_col_id", source_column_id)
            print("dest_col_id", destination_column_id)

            # task_order = Task.objects.filter(column=destination_column_id).count() + 1

            dest_tasks = Task.objects.filter(column=destination_column_id).filter(
                task_order__gte=destination_index
            )

            dest_tasks.update(task_order=F("task_order") + 1)

            print(dest_tasks)

            task_to_update.update(
                column=destination_column_id, task_order=destination_index
            )

            print("task", task_to_update)

            source_tasks = Task.objects.filter(column=source_column_id).filter(
                task_order__gte=source_index
            )
            source_tasks.update(task_order=F("task_order") - 1)
            print(source_tasks)
        else:
            print("else start")
            tasks_to_update = tasks.filter(column=source_column_id)
            if source_index < destination_index:
                # filter tasks from specific column
                print("source < destination")
                tasks_to_update = tasks_to_update.filter(task_order__gte=source_index)
                tasks_to_update = tasks_to_update.filter(
                    task_order__lte=destination_index
                )
                print(tasks_to_update)
                tasks_to_update.update(task_order=F("task_order") - 1)
            else:
                print("source > dest")
                print("dest_index", destination_index)
                tasks_to_update = tasks_to_update.filter(
                    task_order__gte=destination_index
                )
                tasks_to_update = tasks_to_update.filter(task_order__lte=source_index)
                print(tasks_to_update)
                tasks_to_update.update(task_order=F("task_order") + 1)

            task_to_update.update(task_order=destination_index)
            print(task_to_update)

        columns = Column.objects.filter(board=1)

        column_serializer = ColumnSerializer(columns, many=True)
        tasks_serializer = TaskSerializer(tasks, many=True)

        data = {"columns": column_serializer.data, "tasks": tasks_serializer.data}

        return Response(data, status=status.HTTP_200_OK)
