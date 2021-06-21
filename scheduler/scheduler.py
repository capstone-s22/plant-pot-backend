from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ws.ws_server import manager

async def broadcast():
    await manager.broadcast("Hi from server")

scheduler = AsyncIOScheduler()
scheduler.add_job(broadcast, 'interval', seconds=5)
scheduler.start()

