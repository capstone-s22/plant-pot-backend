import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq
from lib.pot import new_pot_registration
from lib.firebase import pots_collection

sys.path.append("..")
from ws.ws_server import ws_manager
from lib.custom_logger import logger
from validations.be2pot_schemas import PotSendDataDictStr, PotSendDataStr, MessageToPot, PotSendDataDictBool, PotSendDataBool

router = APIRouter()

# NOTE: ONLY USED FOR DEV
@router.get('/alertcheckin')
async def health(pot: PotHttpReq):
    try:
        pot_id = pot.id
        # firestore_input = {"session.checkIn.showCheckIn": True}
        # Update Firebase to alert mobile app
        # pots_collection.document(pot_id).update(firestore_input)
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
        logger.error("Check In alert to Pot {} failed!".format(pot_id))
        return {"alert check-in": False}


@router.put('/health')
async def health(pot: PotHttpReq):
    try:
        pot_id = pot.id
        health_check_msg = MessageToPot(
                                potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.health_check,
                                    value="health check"
                                )])
        await ws_manager.send_personal_message_json(health_check_msg.dict(), pot_id)
        logger.info("Health check to pot {} success!".format(pot_id))
        firestore_input = {"connected": True}
        pots_collection.document(pot_id).update(firestore_input)
        return {"health check": True}
    except Exception as e:
        logger.error("Health check to pot {} failed!".format(pot_id))
        return {"health check": False}

@router.post('/add')
async def create(new_pot: PotHttpReq):
    try:
        pot_id = new_pot.id
        if pots_collection.document(pot_id).get().exists:
            logger.info(" Pot {} already registered".format(pot_id))
            return {"success": True, "message": "Pot {} already registered".format(pot_id)}
        else:
            new_pot = new_pot_registration(pot_id, is_pot_connected=(pot_id in ws_manager.check_existing_connections()))
            pots_collection.document(pot_id).set(new_pot.dict())
            logger.info("New Pot {} registered".format(pot_id))
            return {"success": True, "message": "New Pot {} registered".format(pot_id)}
    except Exception as e:
        logger.error(e)
        return f"An Error Occured: {e}"