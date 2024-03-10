from django.db import models
from .User import User



class CountryTechnical(models.Model):
    technical_ref = models.ForeignKey(User,limit_choices_to={'user_type': 'technical'}, on_delete=models.CASCADE)
    country = models.CharField(max_length=155, blank=True,primary_key=True)

class StateTechnical(models.Model):
    technical_ref = models.ForeignKey(User,limit_choices_to={'user_type': 'technical'}, on_delete=models.CASCADE)
    country = models.CharField(max_length=155, blank=True)
    state = models.CharField(max_length=155, blank=True,primary_key=True)

class DistrictTechnical(models.Model):
    technical_ref = models.ForeignKey(User,limit_choices_to={'user_type': 'technical'}, on_delete=models.CASCADE)
    state = models.CharField(max_length=155, blank=True)
    district = models.CharField(max_length=155, blank=True,primary_key=True)

class TechnicalStaff(models.Model):
    technical_ref = models.ForeignKey(User,limit_choices_to={'user_type': 'technical'}, on_delete=models.CASCADE)
    state = models.CharField(max_length=155, blank=True)
    district = models.CharField(max_length=155, blank=True)
    area = models.CharField(max_length=155, blank=True,primary_key=True)
