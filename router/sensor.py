import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq
from models.Sensor import SensorType
from lib.firebase import pots_collection
from validations.be2pot_schemas import MessageToPot, Action, PotSendDataDictStr, PotSendDataStr
from lib.custom_logger import logger

sys.path.append("..")
from ws.ws_server import ws_manager
router = APIRouter()

#TODO: if need be, change payload format to indicate type of sensor
@router.get('/ecsensor')
async def ec_sensor(pot: PotHttpReq):
    try:
        pot_id = pot.id
        response = MessageToPot(action=Action.read,
                                potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=SensorType.nutrient_level,
                                    value="send EC value over")])
        await ws_manager.send_personal_message_json(response.dict(), pot_id)
        logger.info("EC value read message sent to pot {}".format(pot_id))
        return {"success": True}

    except Exception as e:
        logger.error("EC value read message failed to send to pot {}! Message -  ".format(pot_id) + str(e))
        return {"success": False}