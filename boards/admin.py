from django.contrib import admin

from .models import Tag, Task, Board, Column, Label


admin.site.register(Task)
admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Label)
admin.site.register(Tag)
