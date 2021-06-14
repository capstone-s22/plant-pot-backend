from arq.cron import cron
from arq.worker import run_worker

print("Scheduler")

async def my_cron_job(ctx):
    print("I run by myself!")
    
class WorkerSettings:
        cron_jobs = [cron(my_cron_job, hour={2}, minute=20)]

run_worker(WorkerSettings)