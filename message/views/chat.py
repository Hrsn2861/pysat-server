"""views for message.message
"""
from message.models import ChatsHelper
from message.models import ChatBlockHelper
import utils.response as Response

def get_list(package):
    """ get chat list
    """
    user = package.get('user')
    chats = ChatsHelper.get_chats(user['id'])
    blocks = ChatBlockHelper.get_block_list(user['id'])
    chats = [chat for chat in chats if chat['user']['username'] not in blocks]
    msg_count = 0
    for chat in chats:
        msg_count += chat['unread']
    return Response.success_response({
        'chat_count' : len(chats),
        'msg_count' : msg_count,
        'chat_list' : chats
    })
