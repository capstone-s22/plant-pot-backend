import sys
import asyncio
import threading
from typing import Dict
from asgiref.sync import async_to_sync

sys.path.append("..")

from models.Pot import Pot
from models.Plant import Plant, GrowthStage, RingColour
from validations.be2pot_schemas import MessageToPot, PotSendDataDictBool, PotSendDataBool, PotSendDataStr
from ws.ws_server import ws_manager

from lib.firebase import pots_collection

async def listen_collection(collection):
    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    @async_to_sync
    async def on_snapshot(col_snapshot, changes, read_time):
        print("=========")
        for change in changes:
            if change.type.name == 'ADDED':
                print(f'New Pot: {change.document.id}')
            elif change.type.name == 'MODIFIED':
                print(f'Modified Pot: {change.document.id}')
                doc_updated = change.document.__dict__['_data']
                pot_id = change.document.id
                firestore_input = {}

                pot_obj: Pot = Pot.parse_obj(doc_updated)
                
                bool_triggers = {
                    PotSendDataBool.alertLeavesSound: {
                        "fs_path" : "session.reward.rewardSound.{}".format(PotSendDataBool.alertLeavesSound),
                        "value": pot_obj.session.reward.rewardSound.alertLeavesSound
                        },
                    PotSendDataBool.alertCoinsSound: {
                        "fs_path" : "session.reward.rewardSound.{}".format(PotSendDataBool.alertCoinsSound),
                        "value": pot_obj.session.reward.rewardSound.alertCoinsSound
                        }
                    }

                for trigger_field in bool_triggers:
                    if bool_triggers[trigger_field]["value"]:
                        response = MessageToPot(potId=pot_id, 
                                                data=[PotSendDataDictBool(
                                                    field=trigger_field,
                                                    value=True)]
                                                )
                        await ws_manager.send_personal_message_json(response.dict(), pot_id)
                        # TODO: Check if plant pot has to turn it off or will be auto turn off
                        # TODO: Better to have mobile app trigger this by sending to backend directly
                        firestore_input[bool_triggers[trigger_field]["fs_path"]] = False
                
                # NOTE: Should be able to delete this
                # str_triggers = {
                #     PotSendDataStr.harvest: {
                #         "fs_path" : "session.plants",
                #         "value": pot_obj.session.plants
                #         }
                #     }

                # for trigger_field in str_triggers:
                #     if trigger_field == PotSendDataStr.harvest:
                #         current_plants_attr: Dict[RingColour: Plant] = str_triggers[trigger_field]["value"]
                #         for ring_colour in current_plants_attr:
                #             plant: Plant = Plant.parse_obj(current_plants_attr[ring_colour])
                #             if plant.growthStage ==  GrowthStage.harvest:
                #                 print("Pot {}'s plants are ready to harvest!".format(pot_id))
                #                 response = MessageToPot(potId=pot_id, 
                #                                         data=[PotSendDataDictBool(
                #                                             field=trigger_field,
                #                                             value="Pot {}'s plants are ready to harvest!".format(pot_id))])
                #                 await ws_manager.send_personal_message_json(response.dict(), pot_id)
                #                 break

                if firestore_input != {}:
                    pots_collection.document(pot_id).update(firestore_input)

        callback_done.set()

    callback = on_snapshot
    col_watch = collection.on_snapshot(callback)
    # collection.on_snapshot(on_snapshot)


asyncio.ensure_future(listen_collection(pots_collection))

if __name__ == '__main__':
    while True:
        pass