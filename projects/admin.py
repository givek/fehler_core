from django.contrib import admin

from .models import Project, ProjectMembership, Task, Board, Column, Label


admin.site.register(Project)
admin.site.register(ProjectMembership)
admin.site.register(Task)
admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Label)
