from models.CheckIn import CheckIn
from datetime import datetime

def to_add_streak(dt2: datetime, dt1: datetime):
    return 0 <  (dt2 - dt1).days < 2
    
def get_check_in_update(check_in_obj: CheckIn):
    if check_in_obj.checkInLastDate == None:
        check_in_obj.checkInStreak = 1

    else:
        # TODO: Verify if logic is correct (0000 Mon -> 2359 Tue:)
        # NOTE: Add replace(tzinfo=None) to avoid error "can't subtract offset-naive and offset-aware datetimes"
        if to_add_streak(datetime.utcnow(), check_in_obj.checkInLastDate.replace(tzinfo=None)):
            check_in_obj.checkInStreak += 1
        else: 
            check_in_obj.checkInStreak = 1
    check_in_obj.checkInLastDate = datetime.utcnow()
    check_in_obj.showCheckIn = False 

    return check_in_obj.dict()

# test = {'showCheckIn': False, 'checkInStreak': 1, 'checkInLastDate': date(2021, 7, 9, 6, 28, 38, 700010)}
# get_check_in_update(CheckIn.parse_obj(test))