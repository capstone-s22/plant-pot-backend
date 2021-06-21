from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ws.ws_server import manager

async def broadcast():
    await manager.broadcast("Hi from server")

async def daily_check_in_alert():
    await manager.broadcast("CheckIn")

scheduler = AsyncIOScheduler({'apscheduler.timezone': 'UTC'})
# scheduler.add_job(broadcast, 'interval', seconds=5)

scheduler.add_job(broadcast, 'cron', hour=17, minute=55)
scheduler.start()
