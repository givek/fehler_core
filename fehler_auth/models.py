from __future__ import unicode_literals

import uuid
import datetime

from django.shortcuts import reverse
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Invite(models.Model):

    TYPE_OF_MEMBER_CHOICES = [
        ("ADMIN", "Admin"),
        ("PROJECT_MANAGER", "ProjectManager"),
        ("TEAM_LEAD", "TeamLead"),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    member_type = models.CharField(
        max_length=35,
        choices=TYPE_OF_MEMBER_CHOICES,
        default=None,
        blank=True,
        null=True,
    )
    date_sent = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("space", "email")

    def __str__(self):
        return self.email

    def email_invite(self, activation_link, from_email=None, **kwargs):
        subject = "confirm registration"
        message = "please confirm your fehler account " + activation_link
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self, user, space, domain):
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        from .utils import token_generator

        uid64 = urlsafe_base64_encode(force_bytes(user.pk))
        link = reverse(
            "activate",
            kwargs={
                "space_id": space,
                "uid64": uid64,
                "token": token_generator.make_token(user),
            },
        )
        activation_url = "http://" + domain + link

        return activation_url

    def is_valid(self):
        if self.is_active:
            expiration_date = self.date_sent + datetime.timedelta(days=2)
            if expiration_date >= timezone.now():
                return True
        return False
