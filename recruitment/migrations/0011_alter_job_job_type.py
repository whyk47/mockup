# Generated by Django 5.0.4 on 2024-11-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0010_job_job_type_job_remote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Internship', 'Intern')], default='Full Time', max_length=10),
        ),
    ]