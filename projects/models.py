from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE)
    # lead = models.OneToOneField("fehler_auth.User", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(
        "fehler_auth.User",
        through="ProjectMembership",
        related_name="project_members",
    )
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_tasks(self):
        return self.task_set.all()

    def get_members(self):
        return self.members.all()


class ProjectMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey("fehler_auth.User", on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email


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


# Kanban Board


class Board(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(
        "fehler_auth.User",
        on_delete=models.PROTECT,
        related_name="board_owner",
        null=True,
        blank=True,
    )
    members = models.ManyToManyField("fehler_auth.User", related_name="board_members")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Column(models.Model):
    title = models.CharField(max_length=120)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="columns")
    tasks = models.ManyToManyField("Task", related_name="column_tasks")
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
