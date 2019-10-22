"""models for chat block
"""
from django.db import models

from user.models import UserHelper
from .chat import ChatHelper

class Block(models.Model):
    """Program Like Model
    """
    user_id = models.IntegerField()
    chat_id = models.IntegerField()

    class Meta:
        verbose_name = 'chat_block'
        verbose_name_plural = 'chat_blocks'
        get_latest_by = 'id'

class BlockHelper:
    """Chat Block Helper
    """
    @staticmethod
    def check_block(user_id, blocked_user):
        """check if user has blocked a chat
        """
        chat_id = ChatHelper.get_chat(user_id, blocked_user)
        if chat_id is None:
            return None
        blocks = Block.objects.filter(user_id=user_id, chat_id=chat_id)
        return blocks.exists()

    @staticmethod
    def add_block(user_id, blocked_user):
        """add a block
        """
        chat_id = ChatHelper.get_chat(user_id, blocked_user)
        if chat_id is None:
            return None
        if not BlockHelper.check_block(user_id, chat_id):
            Block(user_id=user_id, chat_id=chat_id).save()
        return True

    @staticmethod
    def del_block(user_id, blocked_user):
        """del block
        """
        chat_id = ChatHelper.get_chat(user_id, blocked_user)
        if chat_id is None:
            return None
        blocks = Block.objects.filter(user_id=user_id, chat_id=chat_id)
        blocks.delete()
        return True

    @staticmethod
    def get_block_list(user_id):
        """get block list (return the names of the other users in the blocked chats)
        """
        blocks = Block.objects.filter(user_id=user_id)
        chats = [block.chat_id for block in blocks]
        user_pairs = [ChatHelper.get_chat_users(chat_id) for chat_id in chats]
        user_pairs = [pair for pair in user_pairs if pair is not None]
        user_pairs = [pair for pair in user_pairs if user_id in pair]
        user_ids = [user_1 + user_2 - user_id for user_1, user_2 in user_pairs]
        users = [UserHelper.get_user(user_id) for user_id in user_ids]
        users = [user for user in users if user is not None]
        usernames = [user['username'] for user in users]
        return usernames
