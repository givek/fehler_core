# Generated by Django 2.2.27 on 2022-02-17 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_auto_20220215_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_order',
            field=models.PositiveIntegerField(db_index=True, default=1),
        ),
    ]