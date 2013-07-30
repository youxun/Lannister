from datetime import datetime, timedelta

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore


def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


if __name__ == '__main__':
    scheduler = Scheduler(standalone=True)
    scheduler.add_jobstore(SQLAlchemyJobStore('sqlite:///cron.db'), 'job123')
    alarm_time = datetime.now() + timedelta(seconds=10)
    scheduler.add_date_job(alarm, alarm_time, name='alarm',
                           jobstore='job123', args=[datetime.now()])
    print('To clear the alarms, delete the example.db file.')
    print('Press Ctrl+d to exit')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass