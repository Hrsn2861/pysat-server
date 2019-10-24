"""views for message.message
"""
from user.models import UserHelper
from message.models import ChatHelper
from message.models import MessageHelper
from utils.params import ParamType
import utils.response as Response

def get_list(package):
    """ get message list
    """
    user = package.get('user')
    params = package.get('params')
    friendname = params.get(ParamType.Username)
    friend = UserHelper.get_user_by_username(friendname)
    if friend is None:
        return Response.error_response("Error Username")
    page = params.get(ParamType.Page)
    if page is None:
        page = 1
    page = int(page)
    chat = ChatHelper.get_chat(user['id'], friend['id'])
    if chat:
        ChatHelper.do_read(chat, user['id'])
        count = MessageHelper.get_messages_count(chat)
        messages = MessageHelper.get_messages(chat, page)
        data = {
            'tot_count' : count,
            'now_count' : len(messages),
            'msg_list' : messages
        }
        return Response.success_response(data)
    return Response.checked_response('NoChat')

def send(package):
    """ send message
    """
    user = package.get('user')
    params = package.get('params')
    friendname = params.get(ParamType.Username)
    friend = UserHelper.get_user_by_username(friendname)
    if friend is None:
        return Response.error_response("Error Username")
    content = params.get(ParamType.Content)
    MessageHelper.send_message(user['id'], friend['id'], content)
    chat_id = ChatHelper.get_chat(user['id'], friend['id'])
    ChatHelper.add_message(chat_id, user['id'])
    return Response.checked_response('SendSuccess')

def undo(package):
    """ undo a send
    """
    user = package.get('user')
    params = package.get('params')
    message_id = params.get(ParamType.Id)
    if MessageHelper.undo_message(user['id'], message_id):
        return Response.checked_response('UndoSuccess')
    return Response.error_response('UndoFailed')
