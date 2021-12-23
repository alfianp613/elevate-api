from apscheduler.schedulers.blocking import BlockingScheduler
from sentiment import *
from SVR import *

sched = BlockingScheduler()
koin = ['bitcoin','ethereum','binance coin','tether','solana',
        'cardano','xrp','usd coin','polkadot','dogecoin']

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=10)
def scheduled_job():
    for i in koin:
        sentimen(i)
        forecast_SVR(i)

sched.start()
