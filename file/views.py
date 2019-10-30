"""
module for uploading file
"""
import os
from django.http import HttpResponse


def upload_file_test(request):
    """
    method for uploading
    """
    if request.method == 'POST':
        my_file = request.FILES.get('file', None)
        if not my_file:
            return HttpResponse('no files for upload!')
        destination = open(os.path.join('C:\\Users\\Administrator\\Desktop', my_file.name), 'wb+')
        for chunk in my_file.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse('upload over!')
    return None
