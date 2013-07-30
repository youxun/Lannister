from rest_framework import serializers
from .utils.filesystem import *
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.conf import settings
class File(object):
	def __init__(self,filename,file_path,size):
		self.filename = filename 
		self.file_path = file_path 
		
		path_to_file = os.path.join(self.file_path)
        
		self.size = default_storage.size(path_to_file)

class Directory(object):
	def __init__(self,path,item=None):
		self.path = path
		self.name = os.path.split(path)[1]     
		self.item = item
		self.files = []
		self.dirs = []
		#print path
		dirs, files = default_storage.listdir(path)
		if self.item == None :
			self.item =sum([len(files) for root,dirs,files in os.walk(path)])
		for subdirectory in dirs:
			if subdirectory.startswith('.'):
				continue
			subsubdirectory, subfiles = default_storage.listdir(
                os.path.join(self.path, subdirectory))
			item_count = len(subsubdirectory) + len(subfiles)
			self.dirs.append(subdirectory)

		for file in files:
			if file.startswith('.'):
				continue
			path_to_file = os.path.join(self.path, file)
			size = default_storage.size(path_to_file)
			self.files.append(File(file,path_to_file,size))



class FileURLField(serializers.Field):
	def field_to_native(self,obj,field_name):
		dir_path = obj.__getattribute__(field_name)
		prefix = reverse('filemanager.restviews.dir_list',kwargs={'path':dir_path})
		return settings.HOST_URL+prefix


class FileSerializer(serializers.Serializer):
	filename = serializers.CharField()
	file_path = FileURLField()
	size = serializers.CharField()

	def restore_object(self,attrs,instance=None):
		if instance is None:
			instance.name = attrs.get('filename',instance.name)
			instance.file_path = attrs.get('file_path',instance.file_path)
			instance.size = attrs.get('size',instance.size)
			return instance
		return File(**attrs)

			
class DirField(serializers.Field):
	def field_to_native(self,obj,field_name):
		dir_path = obj.__getattribute__(field_name)
		url_path=[]
		for dir in dir_path:
			prefix = reverse('filemanager.restviews.dir_list',kwargs={'path':dir})
			url_path.append(settings.HOST_URL+prefix)
		return url_path

			
class DirectorySerializer(serializers.Serializer):
	name = serializers.CharField()
	path = FileURLField()
	item = serializers.CharField()
	files = FileSerializer(many = True)
	dirs = DirField()
	#dirs = object.__new__(DirectorySerializer,many = True)
	
	def restore_object(self,attrs,instance=None):
		if instance is None:
			instance.filename = attrs.get('name',instance.name)
			instance.path = attrs.get('path',instance.path)
			instance.item = attrs.get('item',instance.item)
			instance.dirs = attrs.get('dirs',instance.dirs)
			instance.files = attrs.get('files',instance.files)
			return instance
		return Diretory(**attrs)

