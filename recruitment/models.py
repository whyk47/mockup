from django.db import models
from django.contrib.gis.db.models import PointField
from .util import geocode_address
from django.contrib.gis.geos import Point

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    monthly_pay = models.IntegerField()
    address = models.CharField(max_length=300, null=True)
    location = PointField(geography=True, spatial_index=True, null=True)
    company = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        if self.address:
            self.location = Point(geocode_address(self.address))
        super().save(*args, **kwargs)