from django.db import models
from user.models import signup


class Symptoms(models.Model):
    patient = models.ForeignKey(signup, on_delete=models.CASCADE)
    abdPain = models.JSONField(default=list, blank=True)
    anemmia = models.JSONField(default=list, blank=True)
    vomit = models.JSONField(default=list, blank=True)
    diarhea = models.JSONField(default=list, blank=True)
    bmi = models.JSONField(default=list, blank=True)
    cdsAnalysis = models.JSONField(default=list, blank=True)