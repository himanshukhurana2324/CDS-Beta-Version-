from django.db import models

class signup(models.Model):
    username=models.CharField( max_length=100)
    age=models.CharField(max_length=100)
    bloodgroup=models.CharField(max_length=100)
    sex=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.EmailField(primary_key=True,max_length=100)
    state=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    cpassword=models.CharField(max_length=100)

class Symptoms(models.Model):
    patient = models.ForeignKey(signup, on_delete=models.CASCADE)
    abdPain = models.JSONField(default=list, blank=True)
    anemmia = models.JSONField(default=list, blank=True)
    vomit = models.JSONField(default=list, blank=True)
    diarhea = models.JSONField(default=list, blank=True)
    bmi = models.JSONField(default=list, blank=True)
    cdsAnalysis = models.JSONField(default=list, blank=True)