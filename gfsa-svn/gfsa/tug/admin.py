from django.contrib import admin
from tug.models import *
from flight.models import *
import datetime
class GfsaTugsAdmin(admin.ModelAdmin):
    fields = ['tug_identifier','tug_club', 'tug_seat_type', 'tug_text_description', 'tug_initial_flights','tug_initial_flying_hour','tug_flarm_id', 'tug_active']
    list_display = ['tug_identifier','tug_club', 'tug_initial_flights','total_flights','tug_initial_flying_hour','total_flights_hours','tug_flarm_id','tug_status','tug_active']
    search_fields = ['tug_identifier', 'tug_flarm_id', 'tug_club__club_name']
    list_filter = ['tug_club__club_name','tug_status','tug_active']
    actions = ['enable_tugs','disable_tugs']

    def total_flights(self,obj):

        total_flights = GfsaFlightRecords.objects.filter(tug_tug=obj)
        total_flights = obj.tug_initial_flights + len(total_flights)
        return u'%s'  % (total_flights)
    total_flights.short_description = 'Total Launches'  

    def total_flights_hours(self,obj):
        total_flights_hours = 0
        all_flights = GfsaFlightRecords.objects.filter(tug_tug=obj,fr_tug_land__isnull=False)
        for duration in all_flights:
            total_flights_hours += (duration.fr_tug_land-duration.fr_take_off).seconds
        return u'%s'  %  str(datetime.timedelta(seconds=total_flights_hours))
    total_flights_hours.short_description = 'Total Flying Hours'       


    def has_delete_permission(self, request, obj=None):
        return False

    def disable_tugs(modeladmin, request, queryset):
        queryset.update(tug_active=False)
    disable_tugs.short_description = "Disable selected tugs"

    def enable_tugs(modeladmin, request, queryset):
        queryset.update(tug_active=True)
    enable_tugs.short_description = "Enable selected tugs"



admin.site.register(GfsaTugs,GfsaTugsAdmin)