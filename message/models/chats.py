"""specially created for `get chats`
"""
from django.db import models

from utils import date_to_string
from user.models import UserHelper
from .block import BlockHelper
from .chat import Chat

class ChatsHelper:
    """special helper for chats
    """

    @staticmethod
    def empty_function():
        """it's a empty function
        """
        return None

    @staticmethod
    def get_chats(user_id):
        """get the chats by user_id

        return the chaters' info and numbers of unread messages
        """
        qs = Chat.objects.filter(models.Q(user_1=user_id) | models.Q(user_2=user_id))
        qs = qs.order_by("-importance", "-latest_time")
        blocked = BlockHelper.get_block_list(user_id)
        chats = []
        for chat in qs:
            others = UserHelper.get_user(chat.user_1 + chat.user_2 - user_id)
            others = UserHelper.user_filter(others)
            if others is None:
                continue
            othername = others['username']
            if othername in blocked:
                continue
            unread = chat.unread_count
            if chat.latest_sender == user_id:
                unread = 0
            chats.append({
                'user' : others,
                'unread' : unread,
                'time' : date_to_string(chat.latest_time)
            })
        return chats
