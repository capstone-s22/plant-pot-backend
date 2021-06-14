from pydantic import BaseModel
import uuid 
import time as time

from models.User import User
from models.Pot import Pot, PotId
from models.Session import Session, Seed
from models.Pet import Pet
from models.Sensor import Sensor, SensorType, SensorIndicatorRange
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz, quizDifficulty
from models.CheckIn import CheckIn
from models.Activity import Activity

def update_new_session(pot_id, seed_choice, pet_name, pet_type):

    new_pot = Pot(
        pot_id=pot_id,
        pot_registered_time=time.time(),
        sessions={}
        )

    new_session = Session(
        sessionStartTime=time.time(),
        sessionEndTime=None,
        seed=seed_choice,
        pet=Pet(
            name=pet_name,
            type=pet_type
            ),
        )

def new_pot_registration(pot_id):
    new_session_id = str(1)

    new_pot = Pot(
        pot_id=pot_id,
        pot_registered_time=time.time(),
        sessions={}
        )

    new_session = Session(
        session_id = new_session_id,
        sessionStartTime=time.time(),
        sessionEndTime=None,
        seed=None,
        pet=Pet(
            name=None,
            type=None
            ),
        sensors={
            "temperature": Sensor(
                type=SensorType.temperature,
                value=None,
                indicator=None,
                toAlert=False
                ),
            "nutrientLevel": Sensor(
                type=SensorType.nutrient_level,
                value=None,
                indicator=None,
                toAlert=False
                ),
            "waterLevel": Sensor(
                type=SensorType.water_level,
                value=None,
                indicator=None,
                toAlert=False
                )
        },
        greenPointValues=GreenPointValues(
                red= None,
                blue= None,
                yellow= None,
                green= None,
            ),

        reward=Reward(
                coins=80,
                leaves=40,
                coinReward=0,
                leavesReward=0,
            ),

        quiz=Quiz(
            showQuiz=False,
            quizDifficulty=quizDifficulty.easy,
            quizNumber=0,
            quizTooltipDone=False,
            ),

        checkIn=CheckIn(
            checkIn=False,
            checkInStreak=0,
            checkInLastDate=None,
            checkInToopTipDone=False
            ),
        activity=Activity(
            showActivity=False,
            type=None
            )
        )   


    new_pot.sessions[new_session_id]= new_session

    return new_pot.dict()


# new = new_registration("John", "0001", "xiao bai cai", "doggy", "dog")

# print(new)

# # print((new["pots"][0]["sessions"][0]["seed"]))

