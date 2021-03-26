from django.contrib import admin

from .models import User, Invite

admin.site.register(User)
admin.site.register(Invite)
