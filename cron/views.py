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
from math import ceil
from apscheduler.util import convert_to_datetime, timedelta_seconds
from datetime import datetime
import sys
import time
from datetime import *
from apscheduler.scheduler import Scheduler  
import subprocess
class IndexView(View):
    #template_name = 'cron_index.html'
    def get(self,request,*args,**kwargs):
        return render_to_response('cron_index.html')
indexView = IndexView.as_view()


class CreateView(View): 
    @csrf_exempt
    def post(self,request,*args,**kwargs):
        data = request.POST
        parm= _getRecentRuntimes(data)
        name = kwargs['step']
        c = {}
        c.update(csrf(request))
        if name == 'step2':
            print data
            data = {key:data[key][0:len(data[key])] for key in data }
            print data
            c.update(data)
            c.update({'times':parm})
            print c
        elif name == 'step3':
            #if data.cmd != '':
             pass
        else:
             pass
        rc = RequestContext(request,c)
        try:
            return {'step1': lambda:  render_to_response('cron_step1.html',rc),
             'step2': lambda:  render_to_response('cron_step2.html',rc),
             'step3': lambda:  render_to_response('cron_step3.html',rc)}[name]()
        except KeyError:
             raise Http404
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

    
def _tick():
      sys.stdout.write('Tick! The time is: %s\n' % datetime.now()) 

def _getRecentRuntimes(data):
    ap_data = {key:data[key] for key in data if data[key] not in ('*','?')}
    scheduler=Scheduler()
    scheduler.daemonic=False
    myjob=scheduler.add_cron_job(_tick,**ap_data)
    gen= myjob.compute_next_run_time_ex(datetime.now())
    bd = [gen.next() for i in xrange(8)]
    #print bd
    return bd

def _getCommand(pcommand):
    result=subprocess.call(pcommand)

