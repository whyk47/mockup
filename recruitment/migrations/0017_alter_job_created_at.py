# Generated by Django 5.0.4 on 2024-11-14 06:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0016_alter_job_created_at_alter_job_desirable_skills_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]