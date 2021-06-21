from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ws.ws_server import manager

async def broadcast():
    await manager.broadcast("Hi from server")

async def daily_check_in_alert():
    await manager.broadcast("CheckIn")

scheduler = AsyncIOScheduler({'apscheduler.timezone': 'UTC'})

# UTC Time is 8 hours ahead of SGT, so UTC 1600 == SGT 0000
scheduler.add_job(broadcast, 'cron', hour=16)
scheduler.start()
