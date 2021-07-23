from models.Reward import Reward, RewardIncrement
from models.CheckIn import CheckIn
import sys
import os 
from typing import Tuple

from validations.pot2be_schemas import MessageFromPot, Action, PotDataStr, PotDataBool
from validations.be2pot_schemas import MessageToPot, PotSendDataBool, PotSendDataDictStr, PotSendDataStr, PotSendDataDictBool, getPotSendDataBoolSensor
from models.Pot import Pot
from models.Sensor import Sensor, SensorIndicatorRange, SensorType
from lib.pot import new_pot_registration
from lib.firebase import pots_collection
from lib.reward import get_check_in_reward, get_plant_care_reward, get_reward_sounds, get_harvest_reward
from lib.check_in import get_check_in_update
from lib.plant_care import cv_inference, get_harvests_completed, harvest_ready, revise_plants_status, is_sensor_remedy_needed, is_remedy_performed, to_show_trim

from lib.custom_logger import logger

async def crud_manager(message: MessageFromPot):
    pot_id = message.potId
    responses = []
    try:
        # Create
        if message.action == Action.create:
            for pot_data_dict in message.data:
                # Create Pot
                if pot_data_dict.field == PotDataStr.pot:
                    pot_id_to_create = pot_data_dict.value
                    if pots_collection.document(pot_id).get().exists:
                        message = "Pot {} already registered".format(pot_id)
                        logger.info(message)
                    else:
                        new_pot: Pot = new_pot_registration(pot_id_to_create)
                        # Add pot in firebase
                        pots_collection.document(pot_id).set(new_pot.dict())
                        message = "New Pot {} registered".format(pot_id)
                        logger.info(message)

                    ack_response = MessageToPot(potId=pot_id, 
                                            data=[PotSendDataDictStr(
                                                field=PotSendDataStr.acknowledgment,
                                                value=message)]
                                            )
                    responses.append(ack_response)
                    
        #TODO: Create else condition to raise exception if pot not in database
        # Update
        elif message.action == Action.update:
            for pot_data_dict in message.data:
                # Update check-in
                if pot_data_dict.field == PotDataBool.checkIn:
                    # Get plants details
                    pot: Pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
                    if pot.session.checkIn.showCheckIn:
                        check_in_update: CheckIn = get_check_in_update(pot.session.checkIn)
                        check_in_reward: RewardIncrement = get_check_in_reward(pot.session.plants, check_in_update)
                        ring_happy_sound: bool = get_reward_sounds(check_in_reward)
                        firestore_input = {
                            "session.checkIn": check_in_update.dict(),
                            "session.reward.checkInReward": check_in_reward.dict(),
                            "sounds.happySound": ring_happy_sound
                            }
                        check_in_alert_response = MessageToPot(potId=pot_id, 
                                                data=[PotSendDataDictBool(
                                                    field=PotSendDataBool.showCheckIn,
                                                    value=check_in_update.showCheckIn)]
                                                )
                        responses.append(check_in_alert_response)
                    else:
                        raise Exception("Check in not needed")

                # Update sensor values
                # TODO: Refactor: Parse into Sensor Type before converting for firestore input to upload
                elif pot_data_dict.field in [sensor for sensor in SensorType]:
                    sensor_type: SensorType = pot_data_dict.field
                    sensor_value = pot_data_dict.value
                    to_alert, indicator_val = is_sensor_remedy_needed(sensor_type, sensor_value)
                    firestore_input = {
                        "session.sensors.{}.value".format(sensor_type) : sensor_value,
                        "session.sensors.{}.toAlert".format(sensor_type) : to_alert,
                        "session.sensors.{}.indicator".format(sensor_type) : indicator_val.value,
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

                    sensor_alert_response = MessageToPot(potId=pot_id, 
                                            data=[PotSendDataDictBool(
                                                field=getPotSendDataBoolSensor(sensor_type),
                                                value=to_alert)]
                                            )
                    responses.append(sensor_alert_response)

                elif pot_data_dict.field == PotDataStr.image :
                    encoded_img_data = pot_data_dict.value
                    current_pot = Pot.parse_obj(pots_collection.document(pot_id).get().to_dict())
                    new_plants_status = await cv_inference(pot_id, encoded_img_data)
                    logger.info("Plants cv result: {}".format(new_plants_status))
                    # NOTE: Function for time-based plant growth stages. Remove if only depending on CV
                    # TODO: Future work: start time of seed planting based on user indication in app, not session start time
                    # TODO: soundalert here, not through firebase listener
                    new_plants_status = revise_plants_status(current_pot, new_plants_status)
                    new_plants_status = to_show_trim(new_plants_status)

                    # Dont need to check if user indication, users may harvest without using app
                    harvest_count, new_plants_status = get_harvests_completed(current_pot, new_plants_status)
                    harvest_reward = get_harvest_reward(harvest_count)
                    ring_happy_sound = get_reward_sounds(harvest_reward)
                    firestore_input = {
                        "session.plants" : new_plants_status,
                        "session.reward.harvestReward": harvest_reward,
                        "sounds.happySound": ring_happy_sound
                        }

                    harvest_alert_response = MessageToPot(potId=pot_id, 
                                            data=[PotSendDataDictBool(
                                                field=PotSendDataBool.showHarvest,
                                                value=harvest_ready(new_plants_status))])
                    responses.append(harvest_alert_response)

                pots_collection.document(pot_id).update(firestore_input)

        else:
            raise Exception("Invalid Action")

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



