from django.db import models
from django.utils import timezone

from projects.models import Project


class Board(models.Model):
    name = models.CharField(max_length=120)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="board_project",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Column(models.Model):
    title = models.CharField(max_length=120)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="columns")
    tasks = models.ManyToManyField("Task", related_name="column_tasks", blank=True)
    column_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ["column_order"]

    def __str__(self):
        return f"{self.title}"


class Label(models.Model):
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=120)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="labels")

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=120)
    description = models.TextField()
    assignee = models.ForeignKey(
        "fehler_auth.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="task_assignee",
    )
    labels = models.CharField(max_length=120)
    reporter = models.ForeignKey(
        "fehler_auth.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="task_reporter",
    )
    status = models.CharField(max_length=120)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
