# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
# * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GfsaClubs(models.Model):
    club_id = models.IntegerField(unique=True)
    club_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'gfsa_clubs'


class GfsaFlarmRecords(models.Model):
    flmr_id = models.IntegerField(unique=True)
    takeoff_time = models.DateTimeField(blank=True, null=True)
    landing_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gfsa_flarm_records'


class GfsaFlightRecords(models.Model):
    fr_id = models.IntegerField(unique=True)
    xerorecord_xr = models.ForeignKey('GfsaXeroRecord', db_column='XeroRecord_xr_id')  # Field name made lowercase.
    tug_tug = models.ForeignKey('GfsaTugs', db_column='Tug_tug_id')  # Field name made lowercase.
    glider_glider = models.ForeignKey('GfsaGliders', db_column='Glider_glider_id')  # Field name made lowercase.
    fr_p1_id = models.CharField(max_length=45, blank=True)
    fr_p2_id = models.CharField(max_length=45, blank=True)
    fr_p1_pay_percent = models.CharField(max_length=45, blank=True)
    fr_p2_pay_percent = models.CharField(max_length=45, blank=True)
    fr_date = models.CharField(max_length=45, blank=True)
    fr_take_off = models.CharField(max_length=45, blank=True)
    fr_tug_land = models.CharField(max_length=45, blank=True)
    fr_glider_land = models.CharField(max_length=45, blank=True)
    fr_tug_duration = models.CharField(max_length=45, blank=True)
    fr_glider_duration = models.CharField(max_length=45, blank=True)
    fr_special = models.CharField(max_length=45, blank=True)

    class Meta:
        managed = False
        db_table = 'gfsa_flight_records'


class GfsaGliders(models.Model):
    glider_id = models.IntegerField(primary_key=True)
    glider_identifier = models.CharField(unique=True, max_length=45)
    glider_owner = models.CharField(max_length=45)
    glider_total_flights = models.IntegerField(blank=True, null=True)
    glider_total_flying_hour = models.IntegerField(blank=True, null=True)
    glider_seat_type = models.CharField(max_length=45)
    glider_accepted_launch_type = models.CharField(max_length=45)
    glider_other_text_description = models.CharField(max_length=200, blank=True)
    glider_flarm_id = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'gfsa_gliders'


class GfsaSystemConfig(models.Model):
    sc_id = models.IntegerField(unique=True)
    sc_key = models.CharField(max_length=45)
    sc_content = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'gfsa_system_config'


class GfsaTugs(models.Model):
    tug_id = models.IntegerField(unique=True)
    tug_identifier = models.CharField(unique=True, max_length=45)
    tug_owner = models.CharField(max_length=45)
    tug_text_description = models.CharField(max_length=200, blank=True)
    tug_flarm_id = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'gfsa_tugs'


class GfsaUserHasFlightRecord(models.Model):
    user_has_flightrecord_user_user = models.ForeignKey('GfsaUserHasFlightrecordMain',
                                                        db_column='User_has_FlightRecord_User_user_id')  # Field name made lowercase.
    auth_user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'gfsa_user_has_flight_record'


class GfsaUserHasFlightrecordMain(models.Model):
    user_user = models.ForeignKey(AuthUser, db_column='User_user_id', primary_key=True)  # Field name made lowercase.
    flightrecord_fg = models.ForeignKey(GfsaFlightRecords, db_column='FlightRecord_fg_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gfsa_user_has_flightrecord_main'


class GfsaXeroRecord(models.Model):
    xr_id = models.IntegerField(unique=True)
    xr_package = models.CharField(max_length=45, blank=True)

    class Meta:
        managed = False
        db_table = 'gfsa_xero_record'

