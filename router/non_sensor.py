import sys
from fastapi import APIRouter
from models.NonSensor import NonSensorHttpReq
from models.NonSensor import NonSensorType
from lib.firebase import pots_collection
from validations.be2pot_schemas import MessageToPot, Action, PotSendDataDictBool, PotSendDataDictStr, PotSendDataStr
from lib.custom_logger import logger

sys.path.append("..")
from ws.ws_server import ws_manager
router = APIRouter()

@router.put('/fan')
async def ec_sensor(pot: NonSensorHttpReq):
    try:
        pot_id = pot.id
        status: bool = pot.status
        response = MessageToPot(action=Action.update,
                                potId=pot_id, 
                                data=[PotSendDataDictBool(
                                    field=NonSensorType.fan,
                                    value=status)])
        await ws_manager.send_personal_message_json(response.dict(), pot_id)
        logger.info("Fan status message sent to pot {}".format(pot_id))
        return {"success": True}

    except Exception as e:
        logger.error("Fan status message failed to send to pot {}! Message -  ".format(pot_id) + str(e))
        return {"success": False}