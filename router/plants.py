import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq
from lib.firebase import pots_collection
from validations.be2pot_schemas import MessageToPot, Action, PotSendDataDictStr, PotSendDataStr
from lib.custom_logger import logger

sys.path.append("..")
from ws.ws_server import ws_manager
router = APIRouter()

@router.put('/harvest')
async def harvest(pot: PotHttpReq):
    try:
        pot_id = pot.id
        response = MessageToPot(action=Action.read,
                                potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.image,
                                    value="send image over")])
        # TODO: Uncomment once demo is done
        # await ws_manager.send_personal_message_json(response.dict(), pot_id)
        logger.info("CV read message sent to pot {}".format(pot_id))
        return {"success": True}

    except Exception as e:
        logger.error("CV read message failed to send to pot {}! Message -  ".format(pot_id) + str(e))
        return {"success": False}