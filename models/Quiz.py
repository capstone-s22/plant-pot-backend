from pydantic import BaseModel
from enum import Enum

class quizDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Quiz(BaseModel):
    showQuiz: bool
    quizDifficulty: quizDifficulty
    quizNumber: int
    quizTooltipDone: bool

    class Config:  
        use_enum_values = True