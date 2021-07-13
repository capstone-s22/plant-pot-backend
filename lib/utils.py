import time
from datetime import datetime as dt

# TODO: change to simpler method: https://stackoverflow.com/questions/19825330/python-how-to-convert-ctime-to-m-d-y-hms
def dt_float2str(timeDate: float):
    if type(timeDate) == float:
        timeDate = dt.strptime(
            time.ctime(int(timeDate)), "%a %b %d %H:%M:%S %Y"
        ).strftime("%d/%m/%Y %H:%M:%S")

    return timeDate


def dt_str2float(dt_string):
    # TODO: validate datetime string format
    # Sample string value: '04/11/2020 16:30:35'
    if dt_string != "":
        dt_float = dt.strptime(dt_string, "%d/%m/%Y %H:%M:%S").timestamp()
        return dt_float
    else:
        return dt_string

def getCurrentTimeStr():
    return dt_float2str(time.time())

def getCurrentTime():
    return int(time.time())