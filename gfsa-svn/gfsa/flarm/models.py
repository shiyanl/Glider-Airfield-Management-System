from django.db import models
from glider.models import GfsaGliders
from tug.models import GfsaTugs
from flight.models import *

class GfsaFlarmRecords(models.Model):
    id = models.AutoField(primary_key=True)
    flmr_id = models.CharField(max_length=300)
    takeoff_time = models.DateTimeField(max_length=300,blank=True, null=True)
    landing_time = models.DateTimeField(max_length=300,blank=True, null=True)
    flmr_states = models.CharField(max_length=300,blank=True,verbose_name= 'Flarm states')
    class Meta:
        verbose_name_plural = 'Flarm Records'

class GfsaFlarmTimeStamp(models.Model):
    id = models.AutoField(primary_key=True)
    date_stamp = models.DateTimeField(max_length=300,blank=True, null=True)
    class Meta: 
        verbose_name_plural = 'Date Stamp'