import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq
from lib.firebase import pots_collection
from validations.be2pot_schemas import MessageToPot, Action, PotSendDataDictStr, PotSendDataStr

sys.path.append("..")
from ws.ws_server import ws_manager
router = APIRouter()

@router.put('/harvest')
async def harvest(pot: PotHttpReq):
    try:
        pot_id = pot.id
        response = MessageToPot(action=Action.update,
                                potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.image,
                                    value="send image over")])
        await ws_manager.send_personal_message_json(response, pot_id)
        return {"success": True}
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"