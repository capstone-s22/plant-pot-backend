import os
import aiohttp
from ws.pot import new_pot_registration
from validations.schemas import Pot, Message, Action, PotDataStr, PotDataBool, PotDataInt, PotDataDictStr, PotDataDictBool, PotDataDictInt 
from lib.firebase import pots_collection
from scheduler import quiz

CV_SERVER_URL_PREFIX = os.getenv('CV_SERVER_URL_PREFIX')

async def inference(pot_id, encoded_img_data):
    data = { "potId": pot_id, "encoded_data": encoded_img_data }
    async with aiohttp.request(method='GET', url=CV_SERVER_URL_PREFIX, json=data) as resp:
        assert resp.status == 200
        data = await resp.json()
        return data['greenPointVal'], data['yellowPointVal']

async def crud_manager(message: Message):
    pot_id = message.potId
    try:
        # Create
        if message.action == Action.create:
            for pot_data_dict in message.data:
                # Create Pot
                if pot_data_dict["field"] == PotDataStr.pot:
                    pot_id_to_create = pot_data_dict["value"]
                    new_pot: Pot = new_pot_registration(pot_id_to_create)
                    # Add pot in firebase
                    pots_collection.document(pot_id).set(new_pot.dict())
                    # Add quiz trigger dates in firebase
                    # print(new_pot.potRegisteredTime)
                    quiz.schedule_quiz(new_pot.potId, new_pot.potRegisteredTime)
            return "Pod {} created.".format(pot_id)
        
        # Update
        elif message.action == Action.update:
            for pot_data_dict in message.data:
                # Update check-in
                if pot_data_dict["field"] == PotDataBool.checkIn:
                    parameter = "checkIn"
                    show_check_in = pot_data_dict["value"]
                    # TODO: Retrieve latest session if keeping track
                    firestore_input = {"sessions.1.checkIn.showCheckIn".format() : show_check_in}
                    pots_collection.document(pot_id).update(firestore_input)

                # Update sensor values
                elif pot_data_dict["field"] in [sensor for sensor in PotDataInt]:
                    parameter = "Sensor values"
                    sensor_value = pot_data_dict["value"]
                    # TODO: Retrieve latest session if keeping track
                    firestore_input = {"sessions.1.{}.value".format(pot_data_dict["field"]) : sensor_value}
                    pots_collection.document(pot_id).update(firestore_input)

                elif pot_data_dict["field"] == PotDataStr.image :
                    parameter = "Image"
                    encoded_img_data = pot_data_dict["value"]
                    green_point_val, yellow_point_val = await inference(pot_id, encoded_img_data)
                    print(green_point_val, yellow_point_val)

            return "{} for Pot {} updated.".format(parameter, pot_id)
            # return "{} for Pot {} changed to {}.".format(pot_data_dict["field"], pot_id, sensor_value)

        else:
            raise Exception("Invalid Action")
    
    except Exception as e:
        return e

