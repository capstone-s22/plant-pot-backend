import os
import aiohttp
from attr import field

from models.Plant import Plant
from validations.pot2be_schemas import Pot, MessageFromPot, Action, PotDataStr, PotDataBool, PotDataInt, PotDataDictStr, PotDataDictBool, PotDataDictInt 
from validations.be2pot_schemas import MessageToPot, PotSendDataDictStr, PotSendDataStr
from lib.pot import new_pot_registration
from lib.firebase import pots_collection
from lib.reward import get_check_in_reward, get_plant_care_reward, get_reward_sounds
from lib.check_in import get_check_in_update

CV_SERVER_URL_PREFIX = os.getenv('CV_SERVER_URL_PREFIX')

async def inference(pot_id, encoded_img_data):
    data = { "potId": pot_id, "encoded_data": encoded_img_data }
    async with aiohttp.request(method='GET', url=CV_SERVER_URL_PREFIX, json=data) as resp:
        assert resp.status == 200
        response = await resp.json()
        for ring_colour in response:
            try:
                Plant.parse_obj(response[ring_colour]) # Validate data with model
            except Exception as e:
                return e
        return response

async def crud_manager(message: MessageFromPot):
    pot_id = message.potId
    parameter = ""
    try:
        # Create
        if message.action == Action.create:
            for pot_data_dict in message.data:
                # Create Pot
                if pot_data_dict["field"] == PotDataStr.pot:
                    parameter = "pot"
                    pot_id_to_create = pot_data_dict["value"]
                    new_pot: Pot = new_pot_registration(pot_id_to_create)
                    # Add pot in firebase
                    pots_collection.document(pot_id).set(new_pot.dict())

        # Update
        elif message.action == Action.update:
            for pot_data_dict in message.data:
                # Update check-in
                if pot_data_dict["field"] == PotDataBool.checkIn:
                    parameter = "checkIn"

                    # Get plants details
                    pot: Pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
                    if pot.session.checkIn.showCheckIn:
                        check_in_update = get_check_in_update(pot.session.checkIn)
                        check_in_reward = get_check_in_reward(pot.session.plants, check_in_update)
                        reward_sounds = get_reward_sounds(check_in_reward)
                        firestore_input = {
                            "session.checkIn": check_in_update,
                            "session.reward.checkInReward": check_in_reward,
                            "session.reward.rewardSound": reward_sounds
                            }
                    else:
                        raise Exception("Check in not needed")

                # Update sensor values
                elif pot_data_dict["field"] in [sensor for sensor in PotDataInt]:
                    parameter = "Sensor values"
                    sensor_value = pot_data_dict["value"]
                    # TODO: Retrieve latest session if keeping track
                    firestore_input = {"session.{}.value".format(pot_data_dict["field"]) : sensor_value}
                    
                elif pot_data_dict["field"] == PotDataStr.image :
                    parameter = "image"
                    encoded_img_data = pot_data_dict["value"]
                    plant_cv_inference = await inference(pot_id, encoded_img_data)
                    firestore_input = {"session.plants" : plant_cv_inference}
                    
                pots_collection.document(pot_id).update(firestore_input)

        else:
            raise Exception("Invalid Action")

        response = MessageToPot(potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.acknowledgment,
                                    value="{} {}".format(message.action, parameter))]
                                )
        
        return response

    except Exception as e:
        response = MessageToPot(potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.error,
                                    value="Error: {}".format(e))]
                                )
        
        return response



