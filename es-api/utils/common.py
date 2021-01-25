import json
import datetime


def is_json(myjson):
    try:
        if myjson is None:
            return False
        json.dumps(myjson)
        json.loads(json.dumps(myjson))
    except Exception:
        return False
    return True


def have_keys(myjson, *args):
    if is_json(myjson) is False:
        return False
    for arg in args:
        if arg not in myjson:
            return False
    return True


def tokenTime(isrefreshToken: bool):
    timeT = 15
    now = datetime.datetime.now()
    if isrefreshToken is True:
        hours_added = datetime.timedelta(days=timeT)
    else:
        hours_added = datetime.timedelta(minutes=timeT)
    # print("c", hours_added)
    future_date_and_time = now + hours_added
    # print("e", future_date_and_time)
    baseTime = datetime.datetime(
        future_date_and_time.year,
        future_date_and_time.month,
        future_date_and_time.day,
        future_date_and_time.hour,
        future_date_and_time.minute
        ).timestamp()
    # print('datedelta',str(hours_added))
    # print("b", baseTime)
    return baseTime

    # def tokenTime():
    # hours = 2
    # now = datetime.datetime.now()
    # hours_added = datetime.datetime(now.year,now.month,now.day, now.hour+
    # hours,now.minute).timestamp()
    # # print('datedelta',str(hours_added))
    # return hours_added
