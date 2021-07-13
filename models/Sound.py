from pydantic import BaseModel

class Sounds(BaseModel):
    happySound: bool = False
    sadSound: bool = False