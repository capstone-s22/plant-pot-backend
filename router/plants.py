import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq
from lib.firebase import pots_collection
from validations.be2pot_schemas import MessageToPot, Action, PotSendDataDictStr, PotSendDataStr
from lib.custom_logger import logger
from lib.reward import get_harvest_reward

from models.Plant import Plant, GrowthStage, RingColour

sys.path.append("..")
from ws.ws_server import ws_manager
router = APIRouter()

@router.put('/harvest')
async def harvest(pot: PotHttpReq):
    try:
        pot_id = pot.id
        # TODO: Uncomment once demo is done
        # response = MessageToPot(action=Action.read,
        #                         potId=pot_id, 
        #                         data=[PotSendDataDictStr(
        #                             field=PotSendDataStr.image,
        #                             value="send image over")])
        # await ws_manager.send_personal_message_json(response.dict(), pot_id)

        #TODO: Delete this once demo is done
        harvest_count = 1
        harvest_reward = get_harvest_reward(harvest_count)
        ring_colour = RingColour.peach
        plant_update = Plant(ringColour=ring_colour, growthStage=None).dict()
        firestore_input = {
            "session.plants.{}".format(ring_colour): plant_update,
            "session.reward.harvestReward": harvest_reward,
            }
        pots_collection.document(pot_id).update(firestore_input)
        ###########################################

        logger.info("CV read message sent to pot {}".format(pot_id))
        return {"success": True}

    except Exception as e:
        logger.error("CV read message failed to send to pot {}! Message -  ".format(pot_id) + str(e))
        return {"success": False}