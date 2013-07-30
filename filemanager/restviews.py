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
from filemanager.serializers import *	
from .utils.views import *
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

#incept the HttpResponse
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)




'''
class FileUploadView(APIView):
	parser_classes = (FileUploadParser,)
	def put(self, request, filename,format=None):
		print filename
		file_obj = request.FILES['file']
		default_storage.save('temp/test.tmp', ContentFile(file_obj.read()))
		return Response(status=204)
	def post(self,request,format=None):
		request.upload_handlers.insert(0, ProgressUploadHandler(request, outPath))
		upload_file = request.FILES.get('file', None)   # start the upload
		default_storage.save('temp/test1.tmp', ContentFile(file_obj.read()))
		return Response(status=204)
fileuploadview=FileUploadView.as_view()
'''




class Dir_List(APIView):
	def get(self, request,*args,**kwargs):
		path = urllib.unquote(self.kwargs.get('path', ''))
		if not default_storage.exists(path):
			return Response({'msg':'file error'},status=status.HTTP_400_BAD_REQUEST)
		#print path
		directorys = Directory(path)
		serializer = DirectorySerializer(directorys)
		#print serializer.data
		return Response(serializer.data)
	'''
	def post(self,request)
		data = request.DATA
		data = data.strip().replace('\\',"/")
		try:
			default_storage.mkdir(os.path.join(self.get_path(), data))
			return Response({'path':os.path.join(self.get_path(), data)}, status=status.HTTP_201_CREATED)
		except (SuspiciousOperation, OSError) as e:
			return Response({'newdir': new_dir, 'error': e}, status=status.HTTP_400_BAD_REQUEST)
	'''
dir_list = Dir_List.as_view()

	

