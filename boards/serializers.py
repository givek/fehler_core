from rest_framework import serializers

from .models import Task, Board, Column, Label


class TaskSerializer(serializers.ModelSerializer):
    reporter = serializers.CharField(source="reporter.get_full_name")
    date_created = serializers.DateTimeField(format="%B, %d %Y")
    column_title = serializers.CharField(source="column.title")
    assignee_name = serializers.CharField(source="assignee.get_full_name")

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "assignee",
            "assignee_name",
            "reporter",
            "date_due",
            "column",
            "column_title",
            "date_created",
        ]


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    columns = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ["id", "name", "columns"]


class ColumnSerializer(serializers.ModelSerializer):
    # board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    tasks = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ["id", "board", "title", "tasks"]

    # def to_representation(self, instance):
    #     row = super(ColumnSerializer, self).to_representation(instance)
    #     row_id = row["id"]
    #     return {f"column-{row_id}": row}


class LabelSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    class Meta:
        model = Label
        fields = ["id", "name", "color", "board"]


# class TasksReorderSerializer(serializers.Serializer):
#     tasks = TaskSerializer()
#     columns = ColumnSerializer()
