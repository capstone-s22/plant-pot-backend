import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq, Pot
from lib.firebase import pots_collection

sys.path.append("..")
from ws.ws_server import ws_manager
from lib.custom_logger import logger
from validations.be2pot_schemas import MessageToPot, PotSendDataDictBool, PotSendDataBool

router = APIRouter()

# Alert Quiz to Pot
@router.put('/alertquiz')
async def alert_quiz(pot: PotHttpReq):
    try:
        pot_id = pot.id
        pot: Pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
        to_alert_quiz = len(pot.session.quiz.quizDayNumbers) != 0

        alert_quiz_message = MessageToPot(
                                potId=pot_id, 
                                data=[PotSendDataDictBool(
                                    field=PotSendDataBool.showQuiz,
                                    value=to_alert_quiz)])
                                    
        await ws_manager.send_personal_message_json(alert_quiz_message.dict(), pot_id)
        message = "Sent quiz alert - {} - to Pot {}".format(to_alert_quiz, pot_id)
        logger.info(message)
        # TODO: Need a message queue for messages not sent to pots with failed websocket connection
        return {"success": True,  "message": message}

    except Exception as e:
        message = "Quiz alert message to Pot {} failed!".format(pot_id)
        logger.error(message + str(e))
        return {"success": False, "message": message}