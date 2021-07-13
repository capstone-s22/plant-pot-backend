import sys
import os 

from validations.pot2be_schemas import MessageFromPot, Action, PotDataStr, PotDataBool, PotDataFloat, PotDataDictStr, PotDataDictBool, PotDataDictFloat 
from validations.be2pot_schemas import MessageToPot, PotSendDataDictStr, PotSendDataStr, PotSendDataDictBool
from models.Pot import Pot
from models.Sensor import Sensor, SensorType
from lib.pot import new_pot_registration
from lib.firebase import pots_collection
from lib.reward import get_check_in_reward, get_plant_care_reward, get_reward_sounds, get_harvest_reward
from lib.check_in import get_check_in_update
from lib.plant_care import cv_inference, get_harvests_completed, harvest_ready, revise_plants_status, is_sensor_remedy_needed, is_remedy_performed

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
                    parameter = pot_data_dict["field"]
                    pot_id_to_create = pot_data_dict["value"]
                    new_pot: Pot = new_pot_registration(pot_id_to_create)
                    # Add pot in firebase
                    pots_collection.document(pot_id).set(new_pot.dict())

        # Update
        elif message.action == Action.update:
            for pot_data_dict in message.data:
                # Update check-in
                if pot_data_dict["field"] == PotDataBool.checkIn:
                    parameter = pot_data_dict["field"]

                    # Get plants details
                    pot: Pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
                    if pot.session.checkIn.showCheckIn:
                        check_in_update = get_check_in_update(pot.session.checkIn)
                        check_in_reward = get_check_in_reward(pot.session.plants, check_in_update)
                        ring_happy_sound = get_reward_sounds(check_in_reward)
                        firestore_input = {
                            "session.checkIn": check_in_update,
                            "session.reward.checkInReward": check_in_reward,
                            "sounds.happySound": ring_happy_sound
                            }
                    else:
                        raise Exception("Check in not needed")

                # Update sensor values
                # TODO: Refactor: Parse into Sensor Type before converting for firestore input to upload
                elif pot_data_dict["field"] in [sensor for sensor in PotDataFloat]:
                    parameter = pot_data_dict["field"]
                    sensor_type: SensorType = pot_data_dict["field"]
                    sensor_value = pot_data_dict["value"]
                    to_alert = is_sensor_remedy_needed(sensor_type, sensor_value)
                    firestore_input = {
                        "session.sensors.{}.value".format(sensor_type) : sensor_value,
                        "session.sensors.{}.toAlert".format(sensor_type) : to_alert,
                        "sounds.sadSound" : to_alert,
                        }

                    # NOTE: Only need to retrieve latest sensor values if receive healthy values
                    if not to_alert: # sensor is healthy
                        current_pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
                        if is_remedy_performed(sensor_type, current_pot):
                            sensor_remedy_reward = get_plant_care_reward()
                            ring_happy_sound = get_reward_sounds(sensor_remedy_reward)
                            sensor_remedy_firestore_input = {
                                "session.reward.plantCareReward": sensor_remedy_reward,
                                "sounds.happySound": ring_happy_sound
                                }
                            firestore_input.update(sensor_remedy_firestore_input)

                elif pot_data_dict["field"] == PotDataStr.image :
                    parameter = pot_data_dict["field"]
                    encoded_img_data = pot_data_dict["value"]
                    current_pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
                    new_plants_status = await cv_inference(pot_id, encoded_img_data)

                    # NOTE: Function for time-based plant growth stages. Remove if only depending on CV
                    # TODO: Future work: start time of seed planting based on user indication in app, not session start time
                    # TODO: soundalert here, not through firebase listener
                    new_plants_status = revise_plants_status(current_pot, new_plants_status)

                    # Dont need to check if user indication, users may harvest without using app
                    if harvest_ready(new_plants_status):
                        harvest_alert = MessageToPot(potId=pot_id, 
                                                data=[PotSendDataDictBool(
                                                    field=PotSendDataStr.harvest,
                                                    value="Pot {}'s plants are ready to harvest!".format(pot_id))])
                        # await ws_manager.send_personal_message_json(harvest_alert.dict(), pot_id)
                        responses.append(harvest_alert)

                    harvest_count, new_plants_status = get_harvests_completed(current_pot, new_plants_status)
                    harvest_reward = get_harvest_reward(harvest_count)
                    ring_happy_sound = get_reward_sounds(harvest_reward)
                    firestore_input = {
                        "session.plants" : new_plants_status,
                        "session.reward.harvestReward": harvest_reward,
                        "sounds.happySound": ring_happy_sound
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
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_response = MessageToPot(potId=pot_id, 
                                data=[PotSendDataDictStr(
                                    field=PotSendDataStr.error,
                                    value="{}: {}, line {}, {}".format(exc_type, fname, exc_tb.tb_lineno, e))]
                                )
        responses.append(err_response)
        return responses



