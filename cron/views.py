# -*- coding: utf-8 -*- 
from django.conf import settings
from django.views.generic.base import TemplateView, View, RedirectView
from django.http import HttpResponse
from django.views.defaults import page_not_found
from django.shortcuts import render_to_response
from django.http import Http404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

class IndexView(View):
    #template_name = 'cron_index.html'
    def get(self,request,*args,**kwargs):
        return render_to_response('cron_index.html')
indexView = IndexView.as_view()


class CreateView(View):
    @csrf_exempt
    def get(self,request,*args,**kwargs):
        name = kwargs['step']
        c = {}
        c.update(csrf(request))
        rc = RequestContext(request,c)
        try:
            return {'step1': lambda:  render_to_response('cron_step1.html',rc),
             'step2': lambda:  render_to_response('cron_step2.html',rc),
             'step3': lambda:  render_to_response('cron_step3.html',rc)}[name]()
        except KeyError:
            raise Http404

createView = CreateView.as_view()
