# Generated by Django 5.0.4 on 2024-11-14 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0011_alter_job_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]