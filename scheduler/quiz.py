
import os
import sys
import base64
from firebase_admin import credentials, firestore, initialize_app
import json
from datetime import datetime, timedelta
from lib.firebase import db

QUIZ_DETAILS = "constants/quizzes.json"
COLLECTION_NAME = "QUIZZES"
QUIZ_COLLECTION = db.collection(COLLECTION_NAME)

def schedule_quiz(pot_id, pot_reg_date):
    # currently using datetime.utcnow() from Pot class
    # CURRENT_DATE = datetime.today() 
    CURRENT_DATE = pot_reg_date
    data = json.load(open(QUIZ_DETAILS))
    quiz_day_intervals = [entry['quizDayNumber'] for entry in data]

    for interval in quiz_day_intervals:
        end_date = (CURRENT_DATE + timedelta(days=interval)).strftime('%Y%m%d')
        firestore_input = {pot_id: {"quizDayNumber": interval}}
        QUIZ_COLLECTION.document(end_date).set(firestore_input, merge=True)

# schedule_quiz("0004",datetime.utcnow()  + timedelta(days=15) )
