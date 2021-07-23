import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq
from lib.firebase import pots_collection

sys.path.append("..")
from ws.ws_server import ws_manager
from lib.custom_logger import logger
from validations.be2pot_schemas import MessageToPot, PotSendDataDictBool, PotSendDataBool

router = APIRouter()

# NOTE: ONLY USED FOR DEV
@router.put('/alertcheckin')
async def alert_check_in(pot: PotHttpReq):
    try:
        pot_id = pot.id
        firestore_input = {"session.checkIn.showCheckIn": True}
        # Update Firebase to alert mobile app
        pots_collection.document(pot_id).update(firestore_input)
        # Alert Pot
        alert_message = MessageToPot(
                                potId=pot_id, 
                                data=[PotSendDataDictBool(
                                    field=PotSendDataBool.showCheckIn,
                                    value=True)])
        await ws_manager.send_personal_message_json(alert_message.dict(), pot_id)
        logger.info("Sent Check In alert to Pot {}".format(pot_id))
        # TODO: Need a message queue for messages not sent to pots with failed websocket connection
        return {"alert check-in": True}

    except Exception as e:
        logger.error("Check In alert to Pot {} failed!".format(pot_id) + str(e))
        return {"alert check-in": False}