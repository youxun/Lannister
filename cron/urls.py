from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('cron.views',
         url('index/$','indexView',name = 'indexView'),
         url('index/(?P<step>\w+)/$','createView',name = 'createView'),
         )




