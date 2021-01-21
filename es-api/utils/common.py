import json
import datetime


def is_json(myjson):
    try:
        if myjson is None:
            return False
        json.dumps(myjson)
        json.loads(json.dumps(myjson))
    except:
        return False
    return True

def have_keys(myjson,*args):
    if is_json(myjson) is False:
        return False
    for arg in args:
        if arg not in myjson:
            return False
    return True

def tokenTime():
    hours = 2
    now = datetime.datetime.now()
    hours_added = datetime.datetime(now.year,now.month,now.day, now.hour+hours,now.minute).timestamp()
    # print('datedelta',str(hours_added))
    return hours_added