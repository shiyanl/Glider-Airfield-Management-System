from django.db import models
from clubs.models import *
# Create your models here.


class GfsaMember(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    email_address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Email Address')
    glider_club = models.ForeignKey(GfsaClubs, blank=False, null=False, verbose_name='Glider Club')

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = 'Member'