"""
module for uploading file
"""
import utils.file as File
import utils.response as Response
from file.models import AttechmentHelper

def test(package):
    """method for uploading
    """
    file = package.get('file')
    if not file:
        return Response.error_response('NoFILE')
    name, pwd = File.store_file(file, 'file')
    AttechmentHelper.add_file(0, pwd, name)
    return Response.checked_response('Upload')
