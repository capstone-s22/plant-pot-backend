import os
import sys
import asyncio
import threading
import base64
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv
import json
from asgiref.sync import async_to_sync

sys.path.append("..")
from ws import ws_pots

load_dotenv()

FIREBASE_CRED = "credentials/plant-pot-firebase-admin.json"
COLLECTION_NAME = "POTS"

def get_firebase_credentials():
    if os.path.exists(FIREBASE_CRED) and os.path.isfile(FIREBASE_CRED):
        print("Credentials JSON file found")
        return FIREBASE_CRED
    else:
        print("Credentials JSON file not found.")
        encoded_cred = os.getenv('FIREBASE_CRED_ENCODED')
        if encoded_cred != None:
            print("Credentials env var found")

            decoded_cred = json.loads(base64.b64decode(encoded_cred))
            return decoded_cred
        else:
            raise Exception("'FIREBASE_CRED_ENCODED' env var undefined.")

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
                print(1)
                pot_id = doc_updated["ID"]
                print(pot_id)
                for field in doc_updated:
                    if type(doc_updated[field]) == bool and doc_updated[field]:
                        print(2)
                        print(field, doc_updated[field])
                        await handle_flag(pot_id, field)
            elif change.type.name == 'REMOVED':
                print(f'Removed Pot: {change.document.id}')

        callback_done.set()

    callback = on_snapshot
    col_watch = collection.on_snapshot(callback)
    # collection.on_snapshot(on_snapshot)

async def handle_flag(pot_id, field):
    await ws_pots.manager.send_personal_message("Alerting you on field: {}".format(field), pot_id)
    print(ws_pots.manager.active_connections)

# Argument can be a dictionary in place of json file
cred = credentials.Certificate(get_firebase_credentials())
default_app = initialize_app(cred)
db = firestore.client()
pots_collection = db.collection(COLLECTION_NAME)

asyncio.ensure_future(listen_collection(pots_collection))


if __name__ == '__main__':
    while True:
        pass