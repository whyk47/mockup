# Generated by Django 5.0.4 on 2024-11-05 01:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0005_rename_monthly_pay_in_thousands_job_monthly_pay"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="address",
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                geography=True, null=True, srid=4326
            ),
        ),
    ]
