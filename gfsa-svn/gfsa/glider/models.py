#Glider models
from django.db import models
from clubs.models import *
from gfsa.settings import *
from flight.models import *
from clubs.models import *
from xero.models import *
class GfsaGliders(models.Model):
    glider_id = models.AutoField(primary_key=True)
    glider_identifier = models.CharField(unique=True, blank=False, null=False, max_length=45,verbose_name="Identifier")
    glider_owner = models.CharField(max_length=500, blank=True, null=True, default="",verbose_name="Owner")
    glider_club = models.ForeignKey(GfsaClubs,blank=True,null=True)
    glider_member = models.ForeignKey(GFSAXeroContactPerson,blank=True,null=True, verbose_name="Owner/Contact")
    glider_initial_flights = models.IntegerField(default=0, blank=False, null=False,verbose_name="Initial Launches")
    glider_initial_flying_hour = models.IntegerField(default=0, blank=False, null=False,verbose_name="Initial Flying Hours")
    glider_total_flights = models.IntegerField(default=0,blank=True, null=True,verbose_name="Total Launches")
    glider_total_flying_hour = models.IntegerField(default=0, blank=True, null=True,verbose_name="Total Flying Hours")
    glider_seat_type = models.CharField(choices=SEAT_TYPE,default='2',max_length=45,blank=False,null=False,verbose_name="Aircraft Seats")

    # glider_accepted_launch_type = models.CharField(max_length=45,verbose_name="Accepted Launch Type")
    glider_other_text_description = models.TextField(max_length=200, blank=True,null=False, verbose_name="Description")
    glider_flarm_id = models.CharField(max_length=200, blank=True,null=False, verbose_name="Flarm Id")
    glider_active = models.BooleanField(default=True, blank=False,null=False, verbose_name="Active")
    glider_status = models.CharField(choices=STATUSES,default='Ready', max_length=100,verbose_name='Current Status')
    def __unicode__(self):
        return u'%s' % (self.glider_identifier)
    class Meta:
        verbose_name_plural = 'Gliders'