from django.db import models
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE)
    # lead = models.OneToOneField("fehler_auth.User", on_delete=models.CASCADE)
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
    user = models.ForeignKey("fehler_auth.User", on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email


class Task(models.Model):
    name = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=120)
    description = models.TextField()
    assignee = models.OneToOneField(
        "fehler_auth.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="task_assignee",
        unique=False
    )
    labels = models.CharField(max_length=120)
    reporter = models.OneToOneField(
        "fehler_auth.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="task_reporter",
        unique=False

    )
    status = models.CharField(max_length=120)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
