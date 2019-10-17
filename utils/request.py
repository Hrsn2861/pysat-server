"""to get some data from request
"""

def get_ip(request):
    """get ip
    """
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip_address = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip_address = request.META['REMOTE_ADDR']
    return ip_address
