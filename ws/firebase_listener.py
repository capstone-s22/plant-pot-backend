import sys
import asyncio
import threading
from asgiref.sync import async_to_sync

sys.path.append("..")

from models.Pot import Pot
from validations.be2pot_schemas import MessageToPot, PotSendDataDictBool, PotSendDataBool
from ws.ws_server import manager

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

                pot_obj: Pot = Pot.parse_obj(doc_updated)
                
                triggers = {
                    PotSendDataBool.alertLeavesSound: {
                        "fs_path" : "session.reward.{}".format(PotSendDataBool.alertLeavesSound),
                        "value": pot_obj.session.reward.rewardSound.alertLeavesSound
                        },
                    PotSendDataBool.alertCoinsSound: {
                        "fs_path" : "session.reward.{}".format(PotSendDataBool.alertCoinsSound),
                        "value": pot_obj.session.reward.rewardSound.alertCoinsSound
                        },
                    }

                for trigger_field in triggers:
                    print(pot_obj.session.reward)
                    if triggers[trigger_field]["value"]:
                        response = MessageToPot(potId=pot_id, 
                                                data=[PotSendDataDictBool(
                                                    field=trigger_field,
                                                    value=True)]
                                                )
                        await manager.send_personal_message_json(response.dict(), pot_id)
                        firestore_input = {triggers[trigger_field]["fs_path"]: False}
                        pots_collection.document(pot_id).update(firestore_input)

        callback_done.set()

    callback = on_snapshot
    col_watch = collection.on_snapshot(callback)
    # collection.on_snapshot(on_snapshot)


asyncio.ensure_future(listen_collection(pots_collection))

if __name__ == '__main__':
    while True:
        pass