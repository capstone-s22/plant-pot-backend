from models.Pot import Pot
from models.Session import Session, NewSessionInput

def new_pot_registration(pot_id):
    try:
        new_pot = Pot(potId=pot_id)
        new_session = Session(
            newSessInput=NewSessionInput(potId=pot_id),
            )   

        new_pot.sessions[new_session.session_id]= new_session

        return new_pot
    except Exception as e:
        print(e)
        return "ERROR"
