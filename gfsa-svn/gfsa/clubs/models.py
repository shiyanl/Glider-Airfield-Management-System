from django.db import models


class GfsaClubs(models.Model):
    club_name = models.CharField(max_length=45, blank=False, null=False, unique=True)
    club_description = models.TextField(max_length=500, blank=True, null=False)

    def __unicode__(self):
        return u'%s' % (self.club_name)

    class Meta:
        verbose_name_plural = 'Clubs'
