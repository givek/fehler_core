from rest_framework import serializers

from .models import Task, Board, Column, Label


class TaskSerializer(serializers.ModelSerializer):
    reporter = serializers.CharField(source="reporter.get_full_name")

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "assignee",
            "reporter",
            "date_due",
            "column",
        ]


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    columns = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ["id", "name", "columns"]


class ColumnSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ["id", "board", "title", "column_order", "tasks"]


class LabelSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    class Meta:
        model = Label
        fields = ["id", "name", "color", "board"]
