import os
import aiohttp
from attr import field
from lib.pot import new_pot_registration
from models.Plant import Plant
from validations.pot2be_schemas import Pot, MessageFromPot, Action, PotDataStr, PotDataBool, PotDataInt, PotDataDictStr, PotDataDictBool, PotDataDictInt 
from validations.be2pot_schemas import MessageToPot, PotSendDataDictStr, PotSendDataStr

from lib.firebase import pots_collection

CV_SERVER_URL_PREFIX = os.getenv('CV_SERVER_URL_PREFIX')

async def inference(pot_id, encoded_img_data):
    data = { "potId": pot_id, "encoded_data": encoded_img_data }
    async with aiohttp.request(method='GET', url=CV_SERVER_URL_PREFIX, json=data) as resp:
        assert resp.status == 200
        response = await resp.json()
        print(1111)
        for ring_colour in response:
            print(response[ring_colour])
            print(Plant.parse_obj(response[ring_colour])) # Validate data with model
        print(2222)
        return response


'''
{
    "blue": {
        "ringColour": "blue",
        "growthStage": "sprouting",
        "plantHealth": 0.5,
        "plantSize": 2.0
    },
    "red": {
        "ringColour": "red",
        "growthStage": "sprouting",
        "plantHealth": 0.5,
        "plantSize": 2.0
    },
    "peach": {
        "ringColour": "peach",
        "growthStage": "sprouting",
        "plantHealth": 0.5,
        "plantSize": 2.0
    },
    "purple": {
        "ringColour": "purple",
        "growthStage": "sprouting",
        "plantHealth": 0.5,
        "plantSize": 2.0
    }
}

'''
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
                    show_check_in = pot_data_dict["value"]
                    # TODO: Retrieve latest session if keeping track
                    firestore_input = {"session.checkIn.showCheckIn".format() : show_check_in}
                    
                # Update sensor values
                elif pot_data_dict["field"] in [sensor for sensor in PotDataInt]:
                    parameter = "Sensor values"
                    sensor_value = pot_data_dict["value"]
                    # TODO: Retrieve latest session if keeping track
                    firestore_input = {"session.{}.value".format(pot_data_dict["field"]) : sensor_value}
                    
                elif pot_data_dict["field"] == PotDataStr.image :
                    parameter = "Image"
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
        return e



