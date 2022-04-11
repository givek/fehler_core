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


class Risk(models.Model):

    # BACKGROUND = (
    #     ("Finance", "Finance"),
    #     ("Operations", "Operations"),
    #     ("Security", "Security"),
    # )

    IMPACT = (("L", "Low"), ("M", "Medium"), ("H", "High"))

    PROBABILITY = (("L", "Low"), ("M", "Medium"), ("H", "High"))

    # PROBABILITY = (
    #     ("0", "0%"),
    #     ("10", "10%"),
    #     ("20", "20%"),
    #     ("30", "30%"),
    #     ("40", "40%"),
    #     ("50", "50%"),
    #     ("60", "60%"),
    #     ("70", "70%"),
    #     ("80", "80%"),
    #     ("90", "90%"),
    #     (
    #         "100",
    #         "100%",
    #     ),  # C = 100 in Roman. Because value can't be more than 2 numbers.
    # )

    name = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    mitigation_action = models.TextField(blank=True, null=True)

    # background = models.CharField(max_length=50, choices=BACKGROUND, blank=False)
    impact = models.CharField(max_length=2, choices=IMPACT, blank=False)
    probability = models.CharField(max_length=2, choices=PROBABILITY, blank=False)

    # probability_percentage = models.CharField(
    #     max_length=3, choices=PROBABILITY, blank=False
    # )
    owner = models.ForeignKey(
        "fehler_auth.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="risk_owner",
    )
    reporter = models.ForeignKey(
        "fehler_auth.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="risk_reporter",
    )
    # status = models.CharField(max_length=120)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    # @property
    # def severity(self):
