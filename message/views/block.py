"""views for message.message
"""
from message.models import ChatBlockHelper
from user.models import UserHelper
from utils.params import ParamType
import utils.response as Response

def get_list(package):
    """ get block list
    """
    user = package.get('user')
    blocks = ChatBlockHelper.get_block_list(user['id'])
    return Response.success_response({'list' : blocks})

def set_block(package):
    """ set block
    """
    user = package.get('user')
    params = package.get('params')
    friendname = params.get(ParamType.Username)
    friend = UserHelper.get_user_by_username(friendname)
    if friend is None:
        return Response.error_response("Error Username")
    ChatBlockHelper.add_block(user['id'], friend['id'])
    return Response.checked_response('Set Success')

def unset_block(package):
    """ unset block
    """
    user = package.get('user')
    params = package.get('params')
    friendname = params.get(ParamType.Username)
    friend = UserHelper.get_user_by_username(friendname)
    if friend is None:
        return Response.error_response("Error Username")
    ChatBlockHelper.del_block(user['id'], friend['id'])
    return Response.checked_response('Unset Success')
