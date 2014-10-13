#Tug models
from django.db import models
from clubs.models import *
from gfsa.settings import *

class GfsaTugs(models.Model):
    tug_id = models.AutoField(primary_key=True)
    tug_identifier = models.CharField(unique=True, max_length=45,verbose_name="Identifier", help_text='Please type in the identifier of the Tug , e.g. VMG')
    tug_club = models.ForeignKey(GfsaClubs,blank=False,null=False,verbose_name='Tug Club', help_text='Choose a club if it is owned by the club, otherwise, choose Others')
    tug_seat_type = models.CharField(choices=SEAT_TYPE,default='1',max_length=45,blank=False,null=False,verbose_name="Aircraft Seats", help_text='Choose how many seats in the Glider')
    tug_initial_flights = models.IntegerField(default=0,blank=False, null=False,verbose_name="Initial Launches", help_text='Type in the history launches e.g. 5')
    tug_initial_flying_hour = models.IntegerField(default=0,blank=False, null=False,verbose_name="Initial Flying Hours", help_text='Type in the history flying hours e.g. 12')
    tug_total_flights = models.IntegerField(default=0,blank=True, null=False,verbose_name="Total Launches")
    tug_total_flying_hour = models.IntegerField(default=0,blank=True, null=False,verbose_name="Total Flying Hours")
    tug_text_description = models.TextField(max_length=200, blank=True,null=False,verbose_name="Description")
    tug_flarm_id = models.CharField(max_length=200,blank=True,null=False,verbose_name="Flarm Id", help_text='Leave it blank if you are not sure')
    tug_active = models.BooleanField(default=True,verbose_name="Active")
    tug_status = models.CharField(choices=STATUSES,default='Ready',max_length=100,verbose_name='Current Status')
    def __unicode__(self):
        return u'%s' % (str(self.tug_identifier))
    class Meta:
        verbose_name_plural = 'Tugs'

       