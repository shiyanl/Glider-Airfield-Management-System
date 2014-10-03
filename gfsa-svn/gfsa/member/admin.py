from django.contrib import admin

from member.models import GfsaMember


class GfsaMemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'glider_club', 'email_address']
    search_fields = ['first_name', 'last_name', 'glider_club__club_name', 'email_address']
    list_per_page = 20
    list_filter = ['glider_club']

# Register your models here.

admin.site.register(GfsaMember, GfsaMemberAdmin)
# admin.site.register(GfsaXeroRecord,GfsaXeroRecordAdmin)
