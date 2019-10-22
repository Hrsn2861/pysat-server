"""models for chat
"""
from django.db import models

from utils import getdate_now
from user.models import UserHelper
from . import ChatBlockHelper

class Chat(models.Model):
    """Chat Model
    """
    user_1 = models.IntegerField()
    user_2 = models.IntegerField()
    latest_time = models.DateTimeField()
    latest_sender = models.IntegerField(default=0)
    unread_count = models.IntegerField(default=0)
    importance = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'chat'
        verbose_name_plural = 'chats'
        get_latest_by = 'id'

class ChatHelper:
    """Chat Helper
    """

    @staticmethod
    def get_chat(user_1, user_2):
        """get the chat built between user_1 and user_2
        """
        if user_1 > user_2:
            user_1, user_2 = user_2, user_1
        chats = Chat.objects.filter(user_1=user_1, user_2=user_2)
        if chats.exists():
            return chats.last().id
        return None

    @staticmethod
    def get_chat_users(chat_id):
        """get the users by chat_id
        """
        chats = Chat.objects.filter(id=chat_id)
        if chats.exists():
            chat = chats.last()
            return chat.user_1, chat.user_2
        return None

    @staticmethod
    def build_chat(user_1, user_2):
        """build chat between user_1 and user_2
        """
        chat_id = ChatHelper.get_chat(user_1, user_2)
        if chat_id is None:
            if user_1 > user_2:
                user_1, user_2 = user_2, user_1
            chat = Chat(user_1=user_1, user_2=user_2, latest_time=getdate_now())
            chat.save()
            chat_id = chat.id
        return chat_id

    @staticmethod
    def add_message(chat_id, user_id):
        """user send a message in a chat
        """
        chats = Chat.objects.filter(id=chat_id)
        if chats.exists():
            chat = chats.last()
            if user_id in [chat.user_1, chat.user_2]:
                chat.latest_time = getdate_now()
                chat.latest_sender = user_id
                chat.unread_count = chat.unread_count + 1
                chat.save()
                return True
        return False

    @staticmethod
    def do_read(chat_id, user_id):
        """user open the chat and read the unread-messages
        """
        chats = Chat.objects.filter(id=chat_id)
        if chats.exists():
            chat = chats.last()
            if user_id in [chat.user_1, chat.user_2]:
                if user_id != chat.latest_sender:
                    chat.unread_count = 0
                    chat.save()
                return True
        return False

    @staticmethod
    def get_chats(user_id):
        """get the chats by user_id

        return the chaters' info and numbers of unread messages
        """
        qs = Chat.objects.filter(models.Q(user_1=user_id) | models.Q(user_2=user_id))
        qs = qs.order_by("-importance", "-latest_time")
        blocked = ChatBlockHelper.get_block_list(user_id)
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
                'unread' : unread
            })
        return chats
