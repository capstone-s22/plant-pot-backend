from pydantic import BaseModel
from enum import Enum

class QuizDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    class Config:  
        use_enum_values = True

class Quiz(BaseModel):
    showQuiz: bool = False
    quizDifficulty: QuizDifficulty = QuizDifficulty.easy
    quizDayNumber: int = 0