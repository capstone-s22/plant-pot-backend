import os
import sys
import asyncio
import threading
import base64
from firebase_admin import credentials, firestore, initialize_app
import json
from models.Pot import Pot
from datetime import datetime

sys.path.append("..")
from ws import ws_server

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
# default_app = initialize_app(cred)
db = firestore.client()
pots_collection = db.collection(COLLECTION_NAME)

# result = pots_collection.where(u'session.session_id', u'==', "1").get()
# result = pots_collection.where('session.session_id', '==', "1").get()
# result = pots_collection.where('session.quiz.quizDates', 'array_contains', "20210626").get()
result = pots_collection.get()

current_date = datetime.utcnow().strftime('%Y%m%d')
# NOTE: For Python, all string fields with an integer value like '1' require ``
retrieved_pots = pots_collection.where('session.quiz.quizDates', 'array_contains', current_date).get()

for pot in retrieved_pots:
    pot_id = pot.to_dict()["potId"]
    quiz_day_number_idx = pot.to_dict()['session']['quiz']['quizDates'].index(current_date)
    quiz_day_number = pot.to_dict()['session']['quiz']['quizDayNumbers'][quiz_day_number_idx]
    current_show_quiz_numbers: list = pot.to_dict()['session']['quiz']['showQuizNumbers']
    print(pot_id, current_show_quiz_numbers)

    # if current_show_quiz_numbers == None:
    #     firestore_input = {"session.quiz.showQuizNumbers": []}
    #     pots_collection.document(pot_id).update(firestore_input)
