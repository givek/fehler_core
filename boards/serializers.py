from rest_framework import serializers

from .models import Task, Board, Column, Label, Tag


class TaskSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(
        source="reporter.get_full_name", required=False
    )
    # date_created = serializers.DateTimeField(format="%B, %d %Y", required=False)
    # date_due = serializers.DateField(format="%B, %d %Y")
    column_title = serializers.CharField(source="column.title", required=False)
    assignee_name = serializers.CharField(
        source="assignee.get_full_name", required=False
    )
    tags = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Tag.objects.all()
    )
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    # date_due = serializers.DateTimeField(format="%B, %d %Y", required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "assignee",
            "assignee_name",
            "reporter",
            "reporter_name",
            "date_due",
            "priority",
            "tags",
            "column",
            "project",
            "column_title",
            "date_created",
        ]

    def to_internal_value(self, data):
        # convert each element in tags list to lowercase
        data["tags"] = list(map(str.lower, data.get("tags", [])))
        for tag_name in data.get("tags", []):
            Tag.objects.get_or_create(name=tag_name)
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BoardSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
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
