from rest_framework import serializers
from cron.models import Job_Info

class Job_InfoSerializer(serializers.Serializer):
	id = serializers.Field()
	job_name = serializers.CharField(max_length = 32)
	content = serializers.CharField(max_length = 256 )
	create_date = serializers.DateTimeField()
	finish_date = serializers.DateTimeField()


	def restore_object(self,attrs,instance=None):
		if instance:
			instance.job_name = attrs.get('job_name',instance.job_name)
			instance.content = attrs.get('content',instance.content)
			instance.create_date = attrs.get('create_date',instance.create_date)
			instance.finish_date = attrs.get('finish_date',instance.finish_date)
			return instance
		return Job_Info(**attrs)

class Job_InfoModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Job_Info
		fields = ('id','job_name','content','create_date','finish_date')
