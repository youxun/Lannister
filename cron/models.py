from django.db import models
from django.conf import settings
from sqlalchemy import Column
from sqlalchemy.types import *
from tool import database 

DataBaseModel = database.DataBaseModel
db_session = database.getSession()

class BaseModel():
	pass

# Create your models here.

class Job_Info( models.Model ):
    job_name = models.CharField(max_length=32)
    content = models.CharField(max_length=256)
    create_date = models.DateTimeField('date Created',auto_now_add=True)
    finish_date = models.DateTimeField('date finished',null=True)

    class Meta:
        ordering = ('create_date',)