from django.contrib import admin
from xero.models import *

class GfsaXeroContactsAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email_address','phone','club', 'in_xero']
    list_display = ['contact_name', 'first_name', 'last_name', 'email_address', 'phone','club',
                    'in_xero']  # , 'last_update_time']
    search_fields = ['first_name', 'last_name', 'email_address','phone','club__club_name','contact_name']
    list_filter = ['last_name', 'club__club_name', 'in_xero']
    actions = ['delete_selected']
    list_per_page = 20


class GfsaXeroItemCodeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
        
    list_display = ['item_code']  # , 'last_update_time']
    search_fields = ['item_code']
    list_per_page = 20
    actions = ['delete_selected']

admin.site.register(GFSAXeroContactPerson, GfsaXeroContactsAdmin)
admin.site.register(GFSAXeroItemCode, GfsaXeroItemCodeAdmin)