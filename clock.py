from apscheduler.schedulers.blocking import BlockingScheduler
from sentiment import *
from SVR import *

sched = BlockingScheduler(timezone='Asia/Bangkok')


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0)
def scheduled_job():
        koin = ['bitcoin','ethereum','binance coin','tether','solana','cardano','xrp','usd coin','polkadot','dogecoin']
        for i in koin: 
                forecast_SVR(i)

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0, minute=5)
def scheduled_job2():
        koin = ['bitcoin','ethereum']
        for i in koin: 
                sentimen(i)
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0, minute=10)
def scheduled_job3():
        koin = ['binance coin','tether']
        for i in koin: 
                sentimen(i)
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0, minute=15)
def scheduled_job4():
        koin = ['solana','cardano']
        for i in koin: 
                sentimen(i)
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0, minute=20)
def scheduled_job5():
        koin = ['xrp','usd coin']
        for i in koin: 
                sentimen(i)
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0, minute=25)
def scheduled_job6():
        koin = ['polkadot','dogecoin']
        for i in koin: 
                sentimen(i)
                

sched.start()
