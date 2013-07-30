# -*- coding: utf-8 -*- 
from django.conf import settings
from django.views.generic.base import TemplateView, View, RedirectView
from django.http import HttpResponse
from django.views.defaults import page_not_found
from django.shortcuts import render_to_response,redirect
from django.http import Http404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token




class IndexView(View):
	def get(self,request,*args,**kwargs):
		template_name = 'chart.html'
		return render_to_response(template_name)
indexView = IndexView.as_view() 
