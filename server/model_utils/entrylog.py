"""EntryLog Helper for pysat-server

* It contains some functions about EntryLog operation.
"""

from server.models import EntryLog
import datetime
import random


def make_entrykey():
    key = ''
    for i in range(128):
        key += chr(random.randint(65, 90))
    return key


def getEntryLogByKey(key):
    """Get the EntryLog whose entrykey is `key`.
    """
    logs = EntryLog.objects.filter(key=key, deadtime__gt=datetime.datetime.now())
    if len(logs) > 0:
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
    key = None
    while key is None or getEntryLogByKey(key) is not None:
        key = make_entrykey()
    EntryLog(userid=userid, key=key, entrytime=datetime.datetime.now(), deadtime=datetime.datetime.now() + datetime.timedelta(days=7)).save()

    return key

