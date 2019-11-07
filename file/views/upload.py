"""
module for uploading file
"""
import os
import pickle
import glob

import utils.file as File
import utils.response as Response
from utils.params import ParamType
from file.models import AttechmentHelper, VideoHelper

def test(package):
    """method for uploading
    """
    file = package.get('file')
    if not file:
        return Response.error_response('NoFILE')
    name, pwd, _ = File.store_file(file.name, file.chunks(), 'file')
    AttechmentHelper.add_file(0, pwd, name)
    return Response.checked_response('Upload')

def start(package):
    """method for start uploading a big file
    """
    params = package.get('params')
    school_id = params.get(ParamType.SchoolId)
    category_id = params.get(ParamType.CategoryId)
    filename = params.get(ParamType.Filename)
    video_title = params.get(ParamType.VideoTitle)
    description = params.get(ParamType.Description)
    key = params.get(ParamType.FileKey)

    filepath = os.path.join('/mnt/media', 'chunks')
    filepath = os.path.join(filepath, key)
    os.makedirs(filepath)
    with open(os.path.join(filepath, 'config'), 'wb') as file:
        pickle.dump((school_id, category_id, filename, video_title, description), file)
    return Response.success_response({'key' : key})

def chunk(package):
    """method for upload a chunk
    """
    params = package.get('params')
    key = params.get(ParamType.FileKey)
    index = params.get(ParamType.ChunkId)
    file = package.get('file')
    if not file:
        return Response.error_response('NoFILE')
    File.store_chunk(key, index, file)
    return Response.checked_response('Success')

def done(package):
    """method for merge chunks
    """
    user = package.get('user')
    params = package.get('params')
    key = params.get(ParamType.FileKey)
    filepath = os.path.join('/mnt/media', 'chunks')
    filepath = os.path.join(filepath, key)
    with open(os.path.join(filepath, 'config'), 'rb') as file:
        (school_id, category_id, filename, video_title, description) = pickle.load(file)
    number = len(glob.glob(os.path.join(filepath, 'chunk') + '*'))
    chunks = ['chunk' + str(i) for i in range(number)]
    _, pwd, filesize = File.store_file(filename, chunks, 'video', filepath)
    VideoHelper.add_video(
        user['id'], video_title, description, filename, pwd, school_id, category_id, filesize)
    return Response.success_response(None)
