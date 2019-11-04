"""
module for uploading file
"""
import os
import pickle

import utils.file as File
import utils.response as Response
from utils import getdate_now, randkey
from utils.params import ParamType
from file.models import AttechmentHelper

def test(package):
    """method for uploading
    """
    file = package.get('file')
    if not file:
        return Response.error_response('NoFILE')
    name, pwd = File.store_file(file.name, file.chunks(), 'file')
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

    filepath = os.path.join('/mnt/media', 'chunks')
    key = getdate_now().strftime('%Y%m%d%H%M%S') + randkey(length=12)
    filepath = os.path.join(filepath, key)
    os.makedirs(filepath)
    with open(os.path.join(filepath, 'config'), 'wb') as file:
        pickle.dump((school_id, category_id, filename, video_title, description), file)
    return Response.success_response({'key' : key})

def chunk(package):
    """method for upload a chunk
    """
    # params = package.get('params')
    # key = params.get(ParamType.FileKey)
    # print('chunk', key)
    request = package# package.get('request')
    for k, _ in request.POST.items():
        print(k)
    print('id' + str(request.POST.get('chunk')))
    print('key' + str(request.POST.get('key')))
    return Response.error_response(str(request.POST.get('key')))

def done(package):
    """method for merge chunks
    """
    params = package.get('params')
    key = params.get(ParamType.FileKey)
    print('key' + str(key))
    return Response.success_response(None)
