from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('chart.views',
         url('index/$','indexView',name = 'indexView'),     
         )


