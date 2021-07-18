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
from lib.custom_logger import logger

async def listen_collection(collection):
    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    @async_to_sync
    async def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            try:
                if change.type.name == 'ADDED':
                    # print(f'New Pot: {change.document.id}')
                    pass
                elif change.type.name == 'MODIFIED':
                    # print(f'Modified Pot: {change.document.id}')
                    doc_updated = change.document.__dict__['_data']
                    pot_id = change.document.id
                    # print(pot_id)
                    

                    pot_obj: Pot = Pot.parse_obj(doc_updated)
                    
                    bool_triggers = {
                        PotSendDataBool.ringHappySound: {
                            "fs_path" : "sounds.happySound",
                            "value": pot_obj.sounds.happySound
                            },
                        PotSendDataBool.ringSadSound: {
                            "fs_path" : "sounds.sadSound",
                            "value": pot_obj.sounds.sadSound
                            }
                        }

                    for trigger_field in bool_triggers:
                        firestore_input = {}
                        if bool_triggers[trigger_field]["value"]:
                            response = MessageToPot(potId=pot_id, 
                                                    data=[PotSendDataDictBool(
                                                        field=trigger_field,
                                                        value=True)]
                                                    )
                            # TODO: Check if plant pot has to turn it off or will be auto turn off
                            # TODO: Better to have mobile app trigger this by sending to backend directly
                            firestore_input[bool_triggers[trigger_field]["fs_path"]] = False
                            pots_collection.document(pot_id).update(firestore_input)
                            # Shifted after reverting value in fireestore so that dont have to do so if sending to pot fails (not the best implementation)
                            await ws_manager.send_personal_message_json(response.dict(), pot_id)

            except Exception as e:
                if e.args[0] == "Websocket for Pot {} not found".format(pot_id):
                    logger.error(e)

        callback_done.set()

    callback = on_snapshot
    col_watch = collection.on_snapshot(callback)
    # collection.on_snapshot(on_snapshot)


asyncio.ensure_future(listen_collection(pots_collection))

if __name__ == '__main__':
    while True:
        pass