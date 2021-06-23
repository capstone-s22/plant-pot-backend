from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ws.ws_server import manager

from scheduler.quiz import QUIZ_COLLECTION

async def broadcast():
    await manager.broadcast("Hi from server")

async def daily_check_in_alert():
    await manager.broadcast("CheckIn")

async def quiz_alert():
    current_date = datetime.utcnow().strftime('%Y%m%d')
    result = QUIZ_COLLECTION.document(current_date).get().to_dict()
    print(result)
    await manager.broadcast("CheckIn")
    # {'6666': {'quizDayNumber': 1}, '7777': {'quizDayNumber': 1}, '8888': {'quizDayNumber': 1}}

scheduler = AsyncIOScheduler({'apscheduler.timezone': 'UTC'})

# UTC Time is 8 hours ahead of SGT, so UTC 1600 == SGT 0000
scheduler.add_job(daily_check_in_alert, 'cron', hour=16)
scheduler.add_job(quiz_alert, 'cron', hour=18, minute=29)
scheduler.start()
