from django.db import models
from django.contrib.gis.db.models import PointField
from .services.location_service.location_service import LocationService

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    monthly_pay = models.IntegerField()
    address = models.CharField(max_length=300, null=True)
    location = PointField(blank=True, null=True, geography=True, srid=4326)
    company = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        loc = LocationService()
        if self.address:
            self.location = loc.geocode(self.address)
        else:
            raise Exception("Address is required")
        super().save(*args, **kwargs)