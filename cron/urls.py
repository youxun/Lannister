from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('cron.views',
         url('index/$','indexView',name = 'indexView'),
         url('index/(?P<step>\w+)/$','createView',name = 'createView'),
         #url('upload/$','uploadView',name = 'uploadView'),
		 url('test/(?P<type>\w+)/$','testView',name = 'testView'),
		 url('list/$','listjobView',name = 'listjobView'),
         )


urlpatterns += patterns('cron.restviews',
	url('rest/job_info/$','job_info_list',name = 'job_info_list'),
	url('rest/job_info/(?P<pk>[0-9]+)/$','job_info_detail',name = 'job_info_detail'),
	)




