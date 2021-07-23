import json

class PotNotFound(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

test = {'a': 1, "b": 2}

try:
    raise PotNotFound(json.dumps(test))
except Exception as e:
    print(e)
