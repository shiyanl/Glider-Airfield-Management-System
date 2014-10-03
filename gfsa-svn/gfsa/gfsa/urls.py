from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from gfsa.settings import *
from gfsa.models import AdminSite
#from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'gfsa.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^flarm_api/', 'flarm.views.flarm_api'),
                       url(r'^flarm_api_all/', 'flarm.views.flarm_api_all'),
                       url(r'^update_contacts/', 'xero.views.get_contacts'),
                       url(r'^update_itemcode/', 'xero.views.get_item_code'),
                       url(r'^compare_members/', 'xero.views.compare_contact'),
                       #url(r'^admin/lookups/', include(ajax_select_urls)),
                       url(r'^send_notification/', 'xero.views.send_notification'),
)
