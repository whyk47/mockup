# Generated by Django 5.0.4 on 2024-11-14 05:58

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0013_alter_job_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='desirable_skills',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='job',
            name='mandatory_skills',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='job',
            name='responsibilities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='job',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 14, 5, 58, 7, 878423, tzinfo=datetime.timezone.utc)),
        ),
    ]
