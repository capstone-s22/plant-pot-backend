from models.Pot import Pot
from models.Session import Session, NewSessionInput
from datetime import timedelta

def scheduled_quiz_dates(start_date, quiz_day_intervals):
    # currently using datetime.utcnow() from Session class
    # pot_reg_date = datetime.today() 
    quiz_dates = []
    for interval in quiz_day_intervals:
        end_date = (start_date + timedelta(days=interval)).strftime('%Y%m%d')
        quiz_dates.append(end_date)
    return quiz_dates

def new_pot_registration(pot_id):
    try:
        new_pot = Pot(potId=pot_id)
        new_session = Session(
            newSessInput=NewSessionInput(potId=pot_id),
            )   

        quiz_dates = scheduled_quiz_dates(new_session.sessionStartTime, new_session.quiz.quizDayNumbers)
        new_session.quiz.quizDates = quiz_dates

        new_pot.sessions[new_session.session_id]= new_session

        return new_pot
    except Exception as e:
        print(e)
        return "ERROR"
