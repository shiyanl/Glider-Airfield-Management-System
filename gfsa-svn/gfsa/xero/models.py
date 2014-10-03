# Xero models
from django.db import models
from clubs.models import GfsaClubs

class GFSAXeroContactPerson(models.Model):
    contact_id = models.CharField(max_length=100, blank=True, null=True, editable=False, verbose_name='Contact ID')
    contact_name = models.CharField(max_length=500, blank=True, null=True, editable=False, verbose_name='XERO Contact Name')
    first_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='First Name', help_text='Please type your first name.')
    last_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Last Name', help_text='Please type your last name.')
    email_address = models.CharField(max_length=500, blank=False, null=False, verbose_name='Email Address', help_text='Please type email address.(xxxx@xxx)')
    club = models.ForeignKey(GfsaClubs, blank=False, null=False, db_column='club_name', verbose_name='Club', help_text='Please select your club.')
    phone = models.CharField(max_length=20, blank=False, null=False, verbose_name="Phone", 
                    help_text='Please type your mobile number with country code and area code(eg:+61412345678).')
    in_xero = models.BooleanField(blank=False, null=False, default=False, verbose_name='In Xero', 
                    help_text='Please select if this member connects to xero.')

    def __unicode__(self):
        return u'%s' % (self.first_name + " " + self.last_name)

    class Meta:
        verbose_name_plural = 'Contacts'


class GFSAXeroItemCode(models.Model):
    id = models.AutoField(primary_key=True)
    item_code_id = models.CharField(max_length=100, blank=False, null=False, verbose_name='Item Code Id') 
    item_code = models.CharField(max_length=100, blank=False, null=False, verbose_name='Item Code')

    def __unicode__(self):
        return u'%s' % (self.item_code)

    class Meta:
        verbose_name_plural = 'Item Code'


