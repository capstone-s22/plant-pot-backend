from pydantic import BaseModel
import uuid 
import time as time

from models.User import User
from models.Pot import Pot, PotId
from models.Session import Session, NewSessionInput
from models.Sensor import Sensor, SensorType, SensorIndicatorRange
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz, QuizDifficulty
from models.CheckIn import CheckIn
from models.Tutorial import Tutorial

# TODO: initialize default values directly in the classes and not here
def new_pot_registration2(pot_id):
    try:
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
                    toAlert=False,
                    sensorCoinsReward=0,
                    sensorLeavesReward=0
                    ),
                "nutrientLevel": Sensor(
                    type=SensorType.nutrient_level,
                    value=None,
                    indicator=None,
                    toAlert=False,
                    sensorCoinsReward=0,
                    sensorLeavesReward=0
                    ),
                "waterLevel": Sensor(
                    type=SensorType.water_level,
                    value=None,
                    indicator=None,
                    toAlert=False,
                    sensorCoinsReward=0,
                    sensorLeavesReward=0
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
                    alertCoinSound=False,
                    alertLeavesSound=False
                    ),

            quiz=Quiz(
                showQuiz=False,
                quizDifficulty=QuizDifficulty.easy,
                quizNumber=0,
                quizTooltipDone=False,
                quizCoinsReward=0
                ),

            checkIn=CheckIn(
                showCheckIn=False,
                checkInStreak=0,
                checkInLastDate=None,
                checkInToopTipDone=False,
                checkInCoinsReward=0,
                checkInLeavesReward=0
                ),
            tutorial=Tutorial(
                showTutorial=False,
                type=None,
                tutorialCoinsReward=0,
                tutorialLeavesReward=0
                )
            )   

        new_pot.sessions[new_session_id]= new_session

        return new_pot.dict()
    except Exception as e:
        print(e)
        return "ERROR"

def new_pot_registration(pot_id):
    try:
        new_pot = Pot(potId=pot_id)
        new_session = Session(
            newSessInput=NewSessionInput(potId=pot_id),
            sensors={
                SensorType.temperature: Sensor(type=SensorType.temperature),
                SensorType.nutrient_level: Sensor(type=SensorType.nutrient_level),
                SensorType.water_level: Sensor(type=SensorType.water_level)
            },
            greenPointValues=GreenPointValues(),
            reward=Reward(),
            quiz=Quiz(),
            checkIn=CheckIn(),
            tutorial=Tutorial()   
            )   

        new_pot.sessions[new_session.session_id]= new_session

        return new_pot.dict()
    except Exception as e:
        print(e)
        return "ERROR"

# new = new_registration("John", "0001", "xiao bai cai", "doggy", "dog")

# print(new)

# # print((new["pots"][0]["sessions"][0]["seed"]))

