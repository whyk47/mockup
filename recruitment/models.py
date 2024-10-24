from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    monthly_pay_in_thousands = models.IntegerField()
    location = models.CharField(max_length=300, null=True)
    company = models.CharField(max_length=100, null=True)