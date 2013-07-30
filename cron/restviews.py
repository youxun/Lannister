from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser,FileUploadParser
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions,renderers
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from cron.models import *
from cron.serializers import *

#incept the HttpResponse
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)




@csrf_exempt
@api_view(['GET','POST'])
def job_info_list(request):
	if request.method == 'GET':
		job_infos = Job_Info.objects.all()
		serializer = Job_InfoModelSerializer(job_infos,many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = Job_InfoModelSerializer(data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status = 201)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
def job_info_detail(request,pk):
	try:
		job_info = Job_Info.objects.get(pk=pk)
	except Job_Info.DoesNotExist:
		return Response(status=status.HTTP_400_BAD_REQUEST)
	
	if request.method == 'GET':
		serializer = Job_InfoModelSerializer(job_info)
		return Response(serializer.data)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = Job_InfoModelSerializer(job_info,data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors,status =  400)
	elif request.method == 'DELETE':
		job_info.delete()
		return Response(status=status.HTTP_400_BAD_REQUEST)