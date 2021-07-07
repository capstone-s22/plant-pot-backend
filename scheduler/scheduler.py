from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ws.ws_server import manager
from lib.firebase import pots_collection

async def broadcast():
    await manager.broadcast("Hi from server")

async def daily_check_in_alert():
    all_pots = pots_collection.get()

    for pot in all_pots:
        pot_id = pot.to_dict()['potId']
        firestore_input = {"session.checkIn.showCheckIn": True}
        # Update Firebase to alert mobile app
        pots_collection.document(pot_id).update(firestore_input)
        # Alert Pot
        await manager.send_personal_message_text("Check In Alert", pot_id)
        print("Sent Check In alert to Pot {}".format(pot_id))
        # TODO: Need a message queue for messages not sent to pots with failed websocket connection

async def quiz_alert():
    current_date = datetime.utcnow().strftime('%Y%m%d')
    # NOTE: For Python, all string fields with an integer value like '1' require ``
    retrieved_pots = pots_collection.where('session.quiz.quizDates', 'array_contains', current_date).get()

    for pot in retrieved_pots:
        pot_id = pot.to_dict()["potId"]
        quiz_day_number_idx = pot.to_dict()['session']['quiz']['quizDates'].index(current_date)
        quiz_day_number = pot.to_dict()['session']['quiz']['quizDayNumbers'][quiz_day_number_idx]
        firestore_input = {"session.quiz.showQuiz": True,
                            "session.quiz.currentQuizDayNumber" : quiz_day_number}
        # Update Firebase to alert mobile app
        pots_collection.document(pot_id).update(firestore_input)
        print("Updated Quiz {} alert for Pot {} to database".format(quiz_day_number, pot_id))
        # Alert Pot
        await manager.send_personal_message_text("Day {} Quiz Alert".format(quiz_day_number), pot_id)
        print("Sent Quiz {} alert to Pot {}".format(quiz_day_number, pot_id))




scheduler = AsyncIOScheduler({'apscheduler.timezone': 'UTC'})

# UTC Time is 8 hours ahead of SGT, so UTC 1600 == SGT 0000
scheduler.add_job(daily_check_in_alert, 'cron', hour=16)
scheduler.add_job(quiz_alert, 'cron', hour=16)
scheduler.start()