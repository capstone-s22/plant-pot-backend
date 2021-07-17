from pydantic import BaseModel
from enum import Enum
from typing import List, Union

class QuizDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Quiz(BaseModel):
    showQuizNumbers: List[int] = []
    quizDifficulty: QuizDifficulty = QuizDifficulty.easy
    currentQuizDayNumber: int = 1 # User will get quiz right after the tutorial, activated by app
    quizDayNumbers: List[int] = [2,3,4,5,6,7,8]
    quizDates: Union[None, List[str]] = None
    class Config:  
        use_enum_values = True