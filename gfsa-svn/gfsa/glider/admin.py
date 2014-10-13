from django.contrib import admin
from glider.models import *
from flight.models import *
import datetime
from ajax_select import make_ajax_field
from ajax_select.admin import AjaxSelectAdmin
from django import forms

class AddGliderForm(forms.ModelForm):
    glider_member = make_ajax_field(GfsaGliders,'glider_member','person')


    class Meta:
        model = GfsaGliders
        fields = ['glider_identifier','glider_club','glider_member','glider_seat_type','glider_initial_flights','glider_initial_flying_hour','glider_other_text_description','glider_flarm_id']



class GfsaGlidersAdmin(admin.ModelAdmin):
    form = AddGliderForm
    search_fields = ['glider_identifier','glider_flarm_id', 'glider_member__first_name','glider_member__last_name', 'glider_club__club_name']
    list_display = ['glider_identifier','glider_club','glider_member','glider_seat_type','total_flights','total_flights_hours','glider_flarm_id','glider_status']
    list_filter = ['glider_status', 'glider_club']
    actions = []
    def total_flights(self,obj):
        glider = GfsaGliders.objects.get(pk=obj.glider_id)
        total_flights = GfsaFlightRecords.objects.filter(glider_glider=obj)


        total_flights = glider.glider_initial_flights + len(total_flights)

        return u'%s'  % (total_flights)
    total_flights.short_description = 'Total Launches'  

    def total_flights_hours(self,obj):
        glider = GfsaGliders.objects.get(pk=obj.glider_id)
        total_flights_hours = glider.glider_initial_flying_hour * 60 * 60
        all_flights = GfsaFlightRecords.objects.filter(glider_glider=obj,fr_glider_land__isnull=False)
        for duration in all_flights:

            total_flights_hours += (duration.fr_glider_land-duration.fr_take_off).seconds
        return u'%s'  %  str(datetime.timedelta(seconds=total_flights_hours))
    total_flights_hours.short_description = 'Total Flying Hours'    

    def has_delete_permission(self, request, obj=None):
        return False

    def disable_gliders(modeladmin, request, queryset):
        queryset.update(glider_active=False)
    disable_gliders.short_description = "Disable selected gliders"

    def enable_gliders(modeladmin, request, queryset):
        queryset.update(glider_active=True)
    enable_gliders.short_description = "Enable selected gliders"

admin.site.register(GfsaGliders,GfsaGlidersAdmin)
if TEST_FLARM == False:
    admin.site.disable_action('delete_selected')