# Generated by Django 2.2.13 on 2021-03-24 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fehler_auth", "0003_invite_space"),
    ]

    operations = [
        migrations.AddField(
            model_name="invite",
            name="member_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ADMIN", "Admin"),
                    ("PROJECT_MANAGER", "ProjectManager"),
                    ("TEAM_LEAD", "TeamLead"),
                ],
                default=None,
                max_length=35,
                null=True,
            ),
        ),
    ]
