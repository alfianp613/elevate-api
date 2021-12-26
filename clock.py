from apscheduler.schedulers.blocking import BlockingScheduler
from sentiment import *
from SVR import *

sched = BlockingScheduler(timezone='Asia/Bangkok')
koin = ['bitcoin','ethereum','binance coin','tether','solana',
        'cardano','xrp','usd coin','polkadot','dogecoin']

@sched.scheduled_job('cron', day_of_week='sun', hour=22, minute=45)
def scheduled_job():
    for i in koin:
        forecast_SVR(i)

sched.start()
