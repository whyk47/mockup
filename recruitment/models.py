from django.db import models
from django.contrib.gis.db.models import PointField
from django.utils import timezone

from .services.location_service.location_service import LocationService

from datetime import timedelta


class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "Full Time"
        PART_TIME = "Part Time"
        INTERN = "Internship"

    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    monthly_pay = models.IntegerField()
    address = models.CharField(max_length=300, null=True, blank=True)
    location = PointField(blank=True, null=True, geography=True, srid=4326)
    company = models.CharField(max_length=100, null=True)
    remote = models.BooleanField(default=False)
    job_type = models.CharField(max_length=10, choices=JobType.choices, default=JobType.FULL_TIME)
    mandatory_skill_list = models.TextField(null=True, blank=True)
    desirable_skill_list = models.TextField(null=True, blank=True)
    responsibility_list = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        loc = LocationService()
        if self.address:
            self.location = loc.get_point(self.address)
        super().save(*args, **kwargs)

    @property
    def time_since_creation(self) -> str:
        delta = timezone.now() - self.created_at
        if delta.days < 1:
            return f'{delta / timedelta(hours=1):.0f}h'
        if delta.days < 31:
            return f'{delta / timedelta(days=1):.0f}d'
        if delta.days < 365:
            return f'{delta / timedelta(days=30):.0f}mo'
        return f'{delta / timedelta(days=365):.0f}y'
    
    @property
    def mandatory_skills(self) -> list[str]:
        return self.mandatory_skill_list.split(';')
    
    @property
    def desirable_skills(self) -> list[str]:
        return self.desirable_skill_list.split(';')
    
    @property
    def responsibilities(self) -> list[str]:
        return self.responsibility_list.split(';')