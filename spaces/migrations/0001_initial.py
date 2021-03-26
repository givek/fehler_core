# Generated by Django 2.2.13 on 2021-03-16 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import spaces.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fehler_auth', '0002_invite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now),),
                (
                    'type_of_member',
                    models.CharField(
                        blank=True,
                        choices=[
                            ('ADMIN', 'Admin'),
                            ('PROJECT_MANAGER', 'ProjectManager'),
                            ('TEAM_LEAD', 'TeamLead'),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    'invite',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='fehler_auth.Invite',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now),),
                (
                    'members',
                    models.ManyToManyField(
                        related_name='space_members',
                        through='spaces.Membership',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'owner',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='space',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='spaces.Space'
            ),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[],
            options={'proxy': True, 'indexes': [], 'constraints': [],},
            bases=('spaces.membership',),
            managers=[('objects', spaces.managers.AdminManager()),],
        ),
        migrations.CreateModel(
            name='ProjectManager',
            fields=[],
            options={'proxy': True, 'indexes': [], 'constraints': [],},
            bases=('spaces.membership',),
            managers=[('objects', spaces.managers.ProjectManagerManager()),],
        ),
        migrations.CreateModel(
            name='TeamLead',
            fields=[],
            options={'proxy': True, 'indexes': [], 'constraints': [],},
            bases=('spaces.membership',),
            managers=[('objects', spaces.managers.TeamLeadManager()),],
        ),
    ]
