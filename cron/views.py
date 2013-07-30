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
from math import ceil
from apscheduler.util import convert_to_datetime, timedelta_seconds
import sys
from datetime import *
import time
from apscheduler.scheduler import Scheduler 
from apscheduler.jobstores.sqlalchemy_store import  SQLAlchemyJobStore
import subprocess,os
from cron.models import Job_Info
from django.db import transaction
from django.views.generic import ListView
from tool.database import SQLITE_ADDRESS


scheduler=Scheduler()
scheduler.daemonic=False
scheduler.add_jobstore(SQLAlchemyJobStore(SQLITE_ADDRESS),'schedulerjobs')
scheduler.start()

class IndexView(View):
    #template_name = 'cron_index.html'
    def get(self,request,*args,**kwargs):
        return render_to_response('cron_index.html')
indexView = IndexView.as_view()

class ListJobView(ListView):
    paginate_by = 5
    context_object_name = 'instances'
    queryset = Job_Info.objects.all()
    template_name = 'job_list.html'
listjobView = ListJobView.as_view()


class CreateView(View):
    @transaction.autocommit
    @csrf_exempt
    def post(self,request,*args,**kwargs):
        data = request.POST
        name = kwargs['step']
        c = {}
        c.update(csrf(request))
        if name == 'step2':
            parm= _getRecentRuntimes(data)
            #print data
            data = {key:data[key][0:len(data[key])] for key in data }
            #print data
            c.update(data)
            c.update({'times':parm})
            #print c
        elif name == 'step3':
            if data.get('command') and data.get('name'):
                content = data.get('command')
                job_name = data.get('name')
                create_date = datetime.fromtimestamp(time.time()) 
                instance = Job_Info(content=content,job_name=job_name,create_date=create_date,finish_date=create_date)
                instance.save()
                return HttpResponse('/cron/list/')
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






@csrf_exempt
def testView(request,type):
    name = type
    result = ''
    if name == 'command':
        data = request.POST
        data = data['command']
        result = _testCommand(data)
        #HttpResponse.set_cookie('csrf_token',c.get('csrf_token')) 
    else:
        pass
    return HttpResponse(result)
#testView = TestView.as_view()
    
def _tick():
      sys.stdout.write('Tick! The time is: %s\n' % datetime.now()) 

def _getRecentRuntimes(data):
    ap_data = {key:data[key] for key in data if data[key] not in ('*','?')}
    myjob=scheduler.add_cron_job(_tick,**ap_data)
    gen= myjob.compute_next_run_time_ex(datetime.now())
    bd = [gen.next() for i in xrange(8)]
    #print bd
    return bd

def _runScheduler(data):
	ap_data = {key:data[key] for key in data if data[key] not in ('*','?')}
	myjob=scheduler.add_cron_job(_tick,jobstore='schedulerjobs',**ap_data)
	


def _getCommand(pcommand):
    result=os.system(pcommand)
    return result

def _testCommand(data):
    return _getCommand(data)


