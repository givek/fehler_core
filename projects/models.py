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
