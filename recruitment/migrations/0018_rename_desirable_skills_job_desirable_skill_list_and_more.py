# Generated by Django 5.0.4 on 2024-11-14 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0017_alter_job_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='desirable_skills',
            new_name='desirable_skill_list',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='mandatory_skills',
            new_name='mandatory_skill_list',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='responsibilities',
            new_name='responsibility_list',
        ),
    ]
