# Flight models
from django.db import models
from glider.models import GfsaGliders
from tug.models import GfsaTugs
from gfsa.settings import *
from xero.models import GFSAXeroContactPerson, GFSAXeroItemCode
from datetime import datetime


class GfsaFlightRecords(models.Model):
    fr_id = models.AutoField(primary_key=True)
    tug_tug = models.ForeignKey(GfsaTugs, blank=False, null=True, db_column='Tug_tug_id', verbose_name='Tug Name',help_text='Select Tug') # Field name made lowercase.
    glider_glider = models.ForeignKey(GfsaGliders, blank=False, null=False, db_column='Glider_glider_id',
                                      verbose_name='Glider Rego', default=0,
                                      help_text='Please type Glider Rego and select')  # Field name made lowercase.

    fr_p1_id = models.ForeignKey(GFSAXeroContactPerson, blank=False, null=False, db_column='fr_p1_id', on_delete=models.PROTECT,
                                 verbose_name='Pilot 1 (in command)', related_name='fr_p1_id',help_text='Please type pilot\'s first name and select')
    fr_p2_id = models.ForeignKey(GFSAXeroContactPerson, blank=True, null=True, db_column='fr_p2_id', on_delete=models.PROTECT,
                                 verbose_name='Pilot 2', related_name='fr_p2_id',help_text='Please type pilot\'s first name and select')

    fr_p1_pay_percent = models.CharField(choices=PAY_PERCENT, max_length=45, blank=True, null=True,
                                         verbose_name='Pilot 1 Payment %',help_text='Enter Appropriate %')
    fr_p2_pay_percent = models.CharField(choices=PAY_PERCENT, max_length=45, blank=True, null=True,
                                         verbose_name='Pilot 2 Payment %',help_text='Enter Appropriate %')
    fr_take_off = models.DateTimeField(blank=True, null=True, verbose_name='Take Off Time')
    fr_tug_land = models.DateTimeField(blank=True, null=True, verbose_name='Tug Landing Time')
    fr_glider_land = models.DateTimeField(blank=True, null=True, verbose_name='Glider Landing TIme')
    fr_tug_duration = models.CharField(max_length=500, blank=True, null=True, verbose_name='Tug Flight Duration')
    fr_glider_duration = models.CharField(max_length=500, blank=True, null=True, verbose_name='Glider Flight Duration')
    fr_created = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Created Time')
    fr_last_updated = models.DateTimeField(auto_now=True, null=False, verbose_name='Last Updated')
    fr_in_xero = models.BooleanField(blank=False, null=False, default=False, editable = False, verbose_name='In Xero')
    fr_sent = models.BooleanField(blank=False, null=False, default=False, editable = False, verbose_name='Sent Notification')
    fr_comment = models.CharField(default='YBSS -',max_length=500, blank=True, null=True, verbose_name='Comments',
                    help_text='Please type your comments.')

    def __unicode__(self):
        return u'%s' % (self.fr_id)

    class Meta:
        verbose_name_plural = 'Initiate A Flight'



class GfsaFlightRecords2(GfsaFlightRecords):
    class Meta:
        proxy = True
        verbose_name_plural = 'Flight Sheet Viewer'
        app_label = 'flight'



class GfsaTugLanding(GfsaFlightRecords):
    class Meta:
        proxy = True
        verbose_name_plural = 'Tug Landing'
        app_label = 'flight'


class GfsaTakeOff(GfsaFlightRecords):
    class Meta:
        proxy = True
        verbose_name_plural = 'Take Off'
        app_label = 'flight'

class GfsaFlightRecordSheet(GfsaFlightRecords):
    class Meta:
        proxy = True
        verbose_name_plural = 'Flight Record Sheet'
        app_label = 'flight'

class GfsaGliderLanding(GfsaFlightRecords):
    class Meta:
        proxy = True
        verbose_name_plural = 'Glider Landing'
        app_label = 'flight'


class GfsaGliderFlarmFlightRecords(models.Model):
    flight_record_id = models.ForeignKey(GfsaFlightRecords, blank=False, null=True)
    flarm_id = models.CharField(max_length=300, blank=False, null=False)
    take_off = models.DateTimeField(blank=True, null=True, verbose_name='Take Off Time')
    landing = models.DateTimeField(blank=True, null=True, verbose_name='Landing Time')
    use_take_off = models.BooleanField(default=False)
    use_landing = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Glider Flight Flarm'

    def __unicode__(self):
        return ''

    def save(self):
        #print "---------------------------------"
        flight = GfsaFlightRecords.objects.get(pk=self.flight_record_id.pk)
        if self.use_take_off:
            flight.fr_take_off = self.take_off
            flight.save()
        if self.use_landing:
            flight.fr_glider_land = self.landing
            flight.save()
        super(GfsaGliderFlarmFlightRecords, self).save()


class GfsaTugFlarmFlightRecords(models.Model):
    flight_record_id = models.ForeignKey(GfsaFlightRecords, blank=False, null=True)
    flarm_id = models.CharField(max_length=300, blank=False, null=False)
    take_off = models.DateTimeField(blank=True, null=True, verbose_name='Take Off Time')
    landing = models.DateTimeField(blank=True, null=True, verbose_name='Landing Time')
    use_take_off = models.BooleanField(default=False)
    use_landing = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Tug Flight Flarm'

    def __unicode__(self):
        return ''

    def save(self):
        flight = GfsaFlightRecords.objects.get(pk=self.flight_record_id.pk)
        if self.use_take_off:
            flight.fr_take_off = self.take_off
            flight.save()
        if self.use_landing:
            flight.fr_tug_land = self.landing
            flight.save()
        super(GfsaTugFlarmFlightRecords,self).save()
