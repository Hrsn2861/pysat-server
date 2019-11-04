"""utils for file manager
"""
import os

from utils import getdate_now, randkey

def store_file(filename, chunks, filetype):
    """ to store a file and return file address
    """
    filepath = os.path.join('/mnt/media', filetype)
    filepath = os.path.join(filepath, getdate_now().strftime('%Y%m/%d/%H%M%S'))
    os.makedirs(filepath)
    _, ftype = os.path.splitext(filename)
    filename = randkey(length=16) + ftype
    pwd = os.path.join(filepath, filename)
    with open(pwd, 'wb+') as dest:
        for chunk in chunks:
            dest.write(chunk)
    return filename, pwd
