import sys

from validations.pot2be_schemas import MessageFromPot, Action, PotDataStr, PotDataBool, PotDataInt, PotDataDictStr, PotDataDictBool, PotDataDictInt 
from validations.be2pot_schemas import MessageToPot, PotSendDataDictStr, PotSendDataStr, PotSendDataDictBool
from models.Pot import Pot
from lib.pot import new_pot_registration
from lib.firebase import pots_collection
from lib.reward import get_check_in_reward, get_plant_care_reward, get_reward_sounds, get_harvest_reward
from lib.check_in import get_check_in_update
from lib.plant_care import cv_inference, get_harvests_completed, harvest_ready

async def crud_manager(message: MessageFromPot):
    pot_id = message.potId
    parameter = ""
    responses = []
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
                    current_pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
                    new_plants_status = await cv_inference(pot_id, encoded_img_data)

                    # Dont need to check if user indication, users may harvest without using app
                    if harvest_ready(new_plants_status):
                        harvest_alert = MessageToPot(potId=pot_id, 
                                                data=[PotSendDataDictBool(
                                                    field=PotSendDataStr.harvest,
                                                    value="Pot {}'s plants are ready to harvest!".format(pot_id))])
                        # await ws_manager.send_personal_message_json(harvest_alert.dict(), pot_id)
                        responses.append(harvest_alert)

                    harvest_count = get_harvests_completed(current_pot, new_plants_status)
                    harvest_reward = get_harvest_reward(harvest_count)
                    reward_sounds = get_reward_sounds(harvest_reward)
                    firestore_input = {
                        "session.plants" : new_plants_status,
                        "session.reward.plantCareReward": harvest_reward,
                        "session.reward.rewardSound": reward_sounds
                        }
                pots_collection.document(pot_id).update(firestore_input)

        else:
            raise Exception("Invalid Action")
        ack_response = MessageToPot(potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.acknowledgment,
                                    value="{} {}".format(message.action, parameter))]
                                )
        responses.append(ack_response)
        return responses

    except Exception as e:
        err_response = MessageToPot(potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.error,
                                    value="Error: {}".format(e))]
                                )
        responses.append(err_response)
        return responses



