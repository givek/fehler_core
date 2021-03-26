from django.db import models


class AdminManager(models.Manager):
    use_in_migrations = True

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(member_type=self.model.ADMIN)


class ProjectManagerManager(models.Manager):
    use_in_migrations = True

    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(member_type=self.model.PROJECT_MANAGER)
        )


class TeamLeadManager(models.Manager):
    use_in_migrations = True

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(member_type=self.model.TEAM_LEAD)
