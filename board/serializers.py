from rest_framework import serializers

from .models import Task, Board, Column, Label


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "name",
            "project",
            "type",
            "description",
            "assignee",
            "labels",
            "reporter",
            "status",
        ]


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Board
        fields = ["name", "id", "owner"]


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
