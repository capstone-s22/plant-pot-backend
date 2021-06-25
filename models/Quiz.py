from pydantic import BaseModel
from enum import Enum
from typing import List, Union

class QuizDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    class Config:  
        use_enum_values = True

class Quiz(BaseModel):
    showQuiz: bool = False
    quizDifficulty: QuizDifficulty = QuizDifficulty.easy
    currentQuizDayNumber: int = 0
    quizDayNumbers: List[int] = [1,3,6,10,13,15,18,22,28,30]
    quizDates: Union[None, List[str]] = None