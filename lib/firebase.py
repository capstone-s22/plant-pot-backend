import os
import threading
import base64
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv

import json

load_dotenv()

FIREBASE_CRED = "credentials/plant-pot-firebase-admin.json"

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


def listen_document(pot_id):
    global to_notify_pot
    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        global to_notify_pot
        for doc in doc_snapshot:
            # for i in (doc.to_dict()):
            #     print(i, doc.to_dict()[i])
            if doc.to_dict()["ToRing"]:
                print(doc.to_dict()["ToRing"])
                print("CHANGE IN VALUE")
                to_notify_pot = True
            else:
                print("no changes")
        # for change in changes:
        #     print(change.__dict__)
        #     print(change.document.__dict__)
        callback_done.set()

    doc_ref = pots_collection.document(pot_id)

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)
    print(doc_watch)

# Argument can be a dictionary in place of json file
cred = credentials.Certificate(get_firebase_credentials())
default_app = initialize_app(cred)
db = firestore.client()
pots_collection = db.collection('POTS')

listen_document("0001")
