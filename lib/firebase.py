import os
import base64
from firebase_admin import credentials, firestore, initialize_app
import json

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

# Argument can be a dictionary in place of json file
cred = credentials.Certificate(get_firebase_credentials())
default_app = initialize_app(cred)
db = firestore.client()
pots_collection = db.collection(COLLECTION_NAME)