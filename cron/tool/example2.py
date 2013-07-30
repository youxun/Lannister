from datetime import datetime, timedelta

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
from sqlalchemy import create_engine
import logging
logging.basicConfig()
def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


if __name__ == '__main__':
    engine = create_engine('sqlite:///example3.db')
    scheduler = Scheduler(standalone=True)
    scheduler.add_jobstore(SQLAlchemyJobStore(engine=engine), 'shelve')
    alarm_time = datetime.now() + timedelta(seconds=100)
    scheduler.add_cron_job(alarm, 
                           jobstore='shelve', second="*",minute="1")
    print('To clear the alarms, delete the example.db file.')
    print('Press Ctrl+C to exit')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass