from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from django.conf import settings
from ..models import *

DB_ADDRESS = 'mysql://sun:123456@127.0.0.1:3306/sreader?charset=utf8'
SQLITE_ADDRESS = 'sqlite:///../../cron.db'
DB_CONFIG = {
    'encoding': 'utf8',
    'echo': settings.DEBUG
}

#mysql_engine = create_engine(DB_ADDRESS, **DB_CONFIG)
sqlite_engine = create_engine(SQLITE_ADDRESS,**DB_CONFIG)

DB_Session = sessionmaker(bind=sqlite_engine)

DataBaseModel = declarative_base()

def getSession():
    return DB_Session()

def create_db():
    # DataBaseModel.metadata.drop_all(mysql_engine)
    DataBaseModel.metadata.create_all(sqlite_engine)