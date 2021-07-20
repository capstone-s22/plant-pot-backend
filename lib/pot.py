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
        # NOTE: Have to call datetime.utcnow() here instead of creating default values in class Session as it will stay as constant
        new_session = Session(
            newSessInput=NewSessionInput(potId=pot_id),
            sessionStartTime=datetime.utcnow()
            )
        # NOTE: Have to call datetime.utcnow() here instead of creating default values in class Pot as it will stay as constant
        # Another way of getting utc time is datetime.now(timezone.utc)
        new_pot = Pot(potId=pot_id, potRegisteredTime=datetime.utcnow(), session=new_session)
        quiz_dates = scheduled_quiz_dates(new_session.sessionStartTime, new_session.quiz.quizDayNumbers)
        new_session.quiz.quizDates = quiz_dates
        return new_pot
    except Exception as e:
        return e
