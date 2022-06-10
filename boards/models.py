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
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="column_board"
    )
    column_order = models.PositiveIntegerField()

    class Meta:
        ordering = ["column_order"]

    def __str__(self):
        return f"{self.title}"


# TODO: check if this model in unused.
class Label(models.Model):
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=120)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="labels")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=24)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Task(models.Model):
    URGENT = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1

    TASK_PRIORITY_CHOICES = (
        (URGENT, "Urgent"),
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    )

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
    column = models.ForeignKey("Column", related_name="tasks", on_delete=models.CASCADE)
    labels = models.CharField(max_length=120)
    reporter = models.ForeignKey(
        "fehler_auth.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="task_reporter",
    )
    status = models.CharField(max_length=120)
    priority = models.IntegerField(default=LOW, choices=TASK_PRIORITY_CHOICES)
    tags = models.ManyToManyField(Tag, related_name="tasks")
    date_created = models.DateTimeField(default=timezone.now)
    date_due = models.DateField(blank=True, null=True)
    task_order = models.PositiveIntegerField(default=1, db_index=True)

    class Meta:
        ordering = ["task_order"]

    def __str__(self):
        return f"{self.name} {self.task_order}"

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            task_order = self.cal_task_order(self.column)
            self.task_order = task_order
        super(Task, self).save(*args, **kwargs)

    def cal_task_order(self, column):
        present_keys = (
            Task.objects.filter(column=column)
            .order_by("-task_order")
            .values_list("task_order", flat=True)
        )
        if present_keys:
            return present_keys[0] + 1
        else:
            return 1
