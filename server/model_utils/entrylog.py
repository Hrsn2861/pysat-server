from server.models import EntryLog
import datetime

def getEntryLogByKey(key):
    logs = EntryLog.objects.filter(key=key, deadtime__gt=datetime.datetime.now())
    if len(logs) > 0:
        ret = {
            'userid' : logs[0].userid,
            'key' : logs[0].key,
            'deadtime' : logs[0].deadtime
        }
        return ret
    else:
        return None