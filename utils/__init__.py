"""utils
"""

import random
from django.utils import timezone

def randkey(length=128):
    """generate a random key
    """
    key = ''
    for _ in range(length):
        key += chr(random.randint(65, 90))
    return key

def getdate_now():
    """get now time
    """
    return timezone.now()

def getdate_later():
    """get later time
    """
    return timezone.now() + timezone.timedelta(days=7)

def getdate_none():
    """get later time
    """
    return timezone.datetime(year=2000, month=1, day=1)

def date_to_string(date):
    """transform a date into string
    """
    if data is None:
        return '-'
    return date.strftime('%Y-%m-%d %H:%M:%S')
