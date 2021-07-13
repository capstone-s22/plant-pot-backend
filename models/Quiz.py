from pydantic import BaseModel
from enum import Enum
from typing import List, Union

class QuizDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Quiz(BaseModel):
    showQuizNumbers: List[bool] = []
    quizDifficulty: QuizDifficulty = QuizDifficulty.easy
    currentQuizDayNumber: int = 1 # User will get quiz right after the tutorial, activated by app
    quizDayNumbers: List[int] = [3,6,10,13,15,18,22,28,30]
    quizDates: Union[None, List[str]] = None
    class Config:  
        use_enum_values = True