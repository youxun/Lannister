from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'site_proj.views.home', name='home'),
    # url(r'^site_proj/', include('site_proj.foo.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('userena.urls')),
)
urlpatterns += patterns('',
    url(r'^cron/',include('cron.urls')),
)
urlpatterns += patterns('',
	url(r'^filemanager/',include('filemanager.urls')),
)

urlpatterns += patterns('',
	url(r'^chart/',include('chart.urls')),
	
	
	)