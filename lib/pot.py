from datetime import timedelta, datetime, timezone

from models.Pot import Pot
from models.Session import Session, NewSessionInput
from lib.custom_logger import logger

def scheduled_quiz_dates(start_date, quiz_day_intervals):
    # currently using datetime.utcnow() from Session class
    # pot_reg_date = datetime.today() 
    quiz_dates = []
    for interval in quiz_day_intervals:
        # Day 1 means day of registration, so need to minus 1
        end_date = (start_date + timedelta(days=interval-1)).strftime('%Y%m%d')
        quiz_dates.append(end_date)
    return quiz_dates

def new_pot_registration(pot_id):
    try:
        new_session = Session(
            newSessInput=NewSessionInput(potId=pot_id),
            )   
        new_pot = Pot(potId=pot_id, session=new_session)
        quiz_dates = scheduled_quiz_dates(new_session.sessionStartTime, new_session.quiz.quizDayNumbers)
        new_session.quiz.quizDates = quiz_dates
        print(1111111)
        print(new_pot.potRegisteredTime)
        print(datetime.now(timezone.utc))
        print(1111)
        return new_pot
    except Exception as e:
        return e
