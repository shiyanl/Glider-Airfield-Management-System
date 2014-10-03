from django.contrib import admin
from clubs.models import *


class GfsaClubsAdmin(admin.ModelAdmin):
    search_fields = ['club_name', 'club_description']
    list_display = ['club_name', 'club_description']


admin.site.register(GfsaClubs, GfsaClubsAdmin)

