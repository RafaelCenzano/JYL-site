from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from datetime import datetime

'''
def print_time():
    print(datetime.now().strftime('%H:%M:%S'))


# create schedule for printing time
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=print_time,
    trigger=IntervalTrigger(minutes=5),
    id='printing_time_job',
    name='Print time every minute',
    replace_existing=True)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
'''