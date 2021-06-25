from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ws.ws_server import manager
from lib.firebase import pots_collection

async def broadcast():
    await manager.broadcast("Hi from server")

async def daily_check_in_alert():
    await manager.broadcast("CheckIn")

async def quiz_alert():
    current_date = datetime.utcnow().strftime('%Y%m%d')
    print(current_date)
    # NOTE: For Python, all string fields with an integer value like '1' require ``
    retrieved_pots = pots_collection.where('sessions.`1`.quiz.quizDates', 'array_contains', current_date).get()
    print(retrieved_pots)
    for pot in retrieved_pots:
        pot_id = pot.to_dict()["potId"]
        quiz_day_number_idx = pot.to_dict()['sessions']['1']['quiz']['quizDates'].index(current_date)
        quiz_day_number = pot.to_dict()['sessions']['1']['quiz']['quizDayNumbers'][quiz_day_number_idx]
        print("Sending quiz alert to {}".format(pot_id))
        await manager.send_personal_message("Day {} Quiz Alert".format(quiz_day_number), pot_id)


scheduler = AsyncIOScheduler({'apscheduler.timezone': 'UTC'})

# UTC Time is 8 hours ahead of SGT, so UTC 1600 == SGT 0000
scheduler.add_job(daily_check_in_alert, 'cron', hour=16)
scheduler.add_job(quiz_alert, 'cron', hour=17, minute=35)
scheduler.start()
