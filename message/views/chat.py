"""views for message.message
"""
from message.models import ChatsHelper
import utils.response as Response

def get_list(package):
    """ get message list
    """
    user = package.get('user')
    chats = ChatsHelper.get_chats(user['id'])
    msg_count = 0
    for chat in chats:
        msg_count += chat['unread']
    return Response.success_response({
        'chat_count' : len(chats),
        'msg_count' : msg_count,
        'chat_list' : chats
    })
