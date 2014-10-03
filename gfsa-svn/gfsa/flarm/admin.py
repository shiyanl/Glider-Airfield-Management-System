from django.contrib import admin
from flarm.models import *
from glider.models import *
from tug.models import *

class GfsaFlarmAdmin(admin.ModelAdmin):
    list_filter = ['takeoff_time','landing_time','flmr_states']
    date_hierarchy = 'landing_time'
    search_fields = ['flmr_id']
    list_display = ['flmr_id','name_of_plane','date','takeoff','landing','flmr_states']
    list_per_page = 50
    def has_add_permission(self,request):
        return False
    def landing(self,obj):
        flarm = GfsaFlarmRecords.objects.get(pk=obj.pk)
        if flarm.landing_time is None:
            return "lost landing"
        return u'%s' % flarm.landing_time.time()
    landing.short_description = 'Landing time'
    landing.admin_order_field = 'landing_time'
    def takeoff(self,obj):
        flarm = GfsaFlarmRecords.objects.get(pk=obj.pk)
        if flarm.takeoff_time is None:
            return "lost takeoff"
        return u'%s' % flarm.takeoff_time.time()
    takeoff.short_description = 'takeoff time'
    takeoff.admin_order_field = 'takeoff_time'
    def date(self,obj):
        flarm = GfsaFlarmRecords.objects.get(pk=obj.pk)
        try:
            return u'%s' % flarm.takeoff_time.date()
        except:
            return u'%s' % flarm.landing_time.date()
    date.admin_order_field = 'takeoff_time'

    def name_of_plane(self,obj):
        flarm = GfsaFlarmRecords.objects.get(pk=obj.pk)
        try:
            glider = GfsaGliders.objects.get(glider_flarm_id=flarm.flmr_id)
            return 'Glider : '+glider.glider_identifier
        except:
            try:
                tug = GfsaTugs.objects.get(tug_flarm_id=flarm.flmr_id)
                return "Tug : "+tug.tug_identifier
            except:
                return 'N/A'
        # except:
        #     return 'not in sys'




class GfsaFlarmTimeStampAdmin(admin.ModelAdmin):
    list_display=['date_stamp']
admin.site.register(GfsaFlarmRecords,GfsaFlarmAdmin)
admin.site.register(GfsaFlarmTimeStamp,GfsaFlarmTimeStampAdmin)
# Register your models here.
