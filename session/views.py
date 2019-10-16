"""views for session
"""
import utils.response as Response

def start_session():
    """do nothing here
    """
    return

def check_session(package):
    """process the request of check session
    """
    return Response.success_response({'user' : package.get('user')})
