"""EntryLog Helper for pysat-server

* It contains some functions about EntryLog operation.
"""

import datetime
import random
from server.models import EntryLog


def randkey(length=128):
    key = ''
    for _ in range(length):
        key += chr(random.randint(65, 90))
    return key


def getEntryLogByKey(key):
    """Get the EntryLog whose entrykey is `key`.
    """
    if key is None or len(key) != 128:
        return None
    logs = EntryLog.objects.filter(key=key, deadtime__gt=datetime.datetime.now())
    if logs is not None and logs.exists():
        log = logs[0]
        log.deadtime = datetime.datetime.now() + datetime.timedelta(days=7)
        log.save()
        ret = {
            'userid' : log.userid,
            'key' : log.key,
            'entrytime' : log.entrytime,
            'deadtime' : log.deadtime
        }
    else:
        ret = None

    return ret


def addEntryLog(userid):
    """Add an EntryLog into database.

    Return a random key.
    """
    nowdate = datetime.datetime.now()
    logs = EntryLog.objects.filter(userid=userid, deadtime__gt=nowdate)
    for log in logs:
        log.deadtime = nowdate
        log.save()

    key = None
    while key is None or getEntryLogByKey(key) is not None:
        key = randkey()

    EntryLog(
        userid=userid,
        key=key,
        entrytime=nowdate,
        deadtime=nowdate + datetime.timedelta(days=7)
    ).save()

    return key
