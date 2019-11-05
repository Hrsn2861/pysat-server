"""utils for file manager
"""
import os

from utils import getdate_now, randkey

def store_file(filename, chunks, filetype, chunkpath=None):
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
            if chunkpath is None:
                dest.write(chunk)
            else:
                with open(os.path.join(chunkpath, chunk), 'rb') as src:
                    dest.write(src.read())
    return filename, pwd

def store_chunk(key, index, file):
    """ to store a chunk
    """
    filepath = os.path.join('/mnt/media', 'chunks')
    filepath = os.path.join(filepath, key)
    with open(os.path.join(filepath, 'chunk' + str(index)), 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
