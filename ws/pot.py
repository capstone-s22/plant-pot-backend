from pydantic import BaseModel
import uuid 
import time as time

from models.User import User
from models.Pot import Pot, PotId
from models.Session import Session, NewSessionInput
from models.Sensor import Sensor, SensorType, SensorIndicatorRange
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz, quizDifficulty
from models.CheckIn import CheckIn
from models.Activity import Activity

# TODO: initialize default values directly in the classes and not here
def new_pot_registration(pot_id):
    new_session_id = str(1)
    new_pot = Pot(
        potId=pot_id,
        potRegisteredTime=time.time(),
        sessions={}
        )
    new_session = Session(
        session_id = new_session_id,
        sessionStartTime=time.time(),
        sessionEndTime=None,
        newSessInput=NewSessionInput(
            potId=pot_id,
            petName=None,
            petType=None,
            seed=None,
            hat=None
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
                coinsReward=0,
                leavesReward=0,
                alertCoinSound=False,
                alertLeavesSound=False
                ),

        quiz=Quiz(
            showQuiz=False,
            quizDifficulty=quizDifficulty.easy,
            quizNumber=0,
            quizTooltipDone=False,
            ),

        checkIn=CheckIn(
            showCheckIn=False,
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

