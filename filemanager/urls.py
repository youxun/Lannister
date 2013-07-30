from django.conf.urls import patterns, include, url

urlpatterns = patterns('filemanager.views',
    url(r'^$', 'frontpage', name='fileserver_frontpage'),
    url(r'^login/$', 'login', name='fileserver_login'),
    url(r'^logout/$', 'logout', name='fileserver_logout'),
    url(r'^todo/$', 'todo', name='fileserver_todo'),
    url(r'^browse/(?P<path>.*)', 'browse', name='fileserver_browse'),
    url(r'^mkdir/(?P<path>.*)', 'mkdir', name='fileserver_mkdir'),
    url(r'^download/(?P<path>.*)', 'download', name='fileserver_download'),
    url(r'^upload/(?P<path>.*)', 'upload', name='fileserver_upload'),
    url(r'^edit/(?P<path>.*)', 'edit_directory', name='fileserver_edit_directory'),
    url(r'^zip/(?P<path>.*)', 'zip_directory', name='fileserver_zip'),

	#url(r'upload/', 'uploadEx', name = 'fileserver_uploadEx' ),
    #url( r'^$', generic.TemplateView.as_view( template_name = 'base.html' ) ),
)

urlpatterns += patterns('filemanager.restviews',
	url(r'^rest/(?P<path>.*)','dir_list',name='dir_list'),
	)
