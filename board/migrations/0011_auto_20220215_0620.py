# Generated by Django 2.2.27 on 2022-02-15 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_auto_20220212_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]