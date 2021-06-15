from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import Union

class DataDict(TypedDict):
    field: str
    value: Union[None, bool, int, str]

class Test(BaseModel):
    data: DataDict

input = {"data": {"field": "showPopUp", "value": True}}
test: Test = Test.parse_obj(input)
print(test.data["value"], type(test.data["value"]))
