from django.contrib import admin

from .models import Project, ProjectMembership, Task


admin.site.register(Project)
admin.site.register(ProjectMembership)
admin.site.register(Task)
