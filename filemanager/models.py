# File required from django

from django.db import models
from django.conf import settings

# Create your models here.

class Photo( models.Model ):
	file = models.FileField(upload_to='/')

