"""views for session
"""
import utils.response as Response

def start_session():
    """do nothing here
    """
    return Response.failed_response('Error')

def check_session(package):
    """process the request of check session
    """
    return Response.success_response({'user' : package.get('user')})
