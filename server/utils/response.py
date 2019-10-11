"""to package the data
"""

from django.http import JsonResponse


def make_response(status, msg, data):
    """make response
    """
    if not isinstance(status, int):
        return None
    if status not in [1, 0, -1]:
        return None
    if not isinstance(msg, str):
        return None
    package = {
        'status' : status,
        'msg' : msg,
        'data' : data
    }
    return JsonResponse(package)


def invalid_request():
    """make an 'invalid request' response
    """
    return make_response(status=-1, msg="InvalidRequest", data=None)


def success_response(data):
    """make a success response
    """
    return make_response(status=1, msg="Success", data=data)


def checked_response(msg):
    """make a error response
    """
    return make_response(status=1, msg=msg, data=None)


def error_response(msg):
    """make a error response
    """
    return make_response(status=0, msg=msg, data=None)


def failed_response(msg):
    """make a failed response
    """
    return make_response(status=-1, msg=msg, data=None)
