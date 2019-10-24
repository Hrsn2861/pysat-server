"""models for message
"""
from django.db import models
from django.utils import timezone

from user.models import UserHelper
from utils import getdate_now, date_to_string
from .chat import ChatHelper

class Message(models.Model):
    """Message Model
    """
    chat_id = models.IntegerField()
    sender = models.IntegerField()
    content = models.TextField()
    send_time = models.DateTimeField()
    valid = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        get_latest_by = 'id'

class MessageHelper:
    """Message Helper
    """

    @staticmethod
    def send_message(sender, reciever, message):
        """send message
        """
        chat_id = ChatHelper.build_chat(sender, reciever)
        message = Message(chat_id=chat_id, sender=sender, content=message, send_time=getdate_now())
        message.save()

    @staticmethod
    def undo_message(user_id, message_id):
        """get messages between user_1 and user_2
        """
        qs = Message.objects.filter(id=message_id, valid=True)
        if not qs.exists():
            return False
        message = qs.last()
        if message.sender != user_id:
            return False
        if message.send_time + timezone.timedelta(seconds=5) < getdate_now():
            return False
        message.valid = False
        message.save()
        return True

    @staticmethod
    def get_messages_count(chat_id):
        """get messages between user_1 and user_2
        """
        qs = Message.objects.filter(chat_id=chat_id, valid=True)
        return qs.count()

    @staticmethod
    def get_messages(chat_id, page):
        """get messages between user_1 and user_2
        """
        messages = []
        qs = Message.objects.filter(chat_id=chat_id, valid=True)
        qs = qs.order_by('-id')
        qs = qs[(page - 1) * 20 : page * 20]
        usernames = {}
        for message in qs:
            if usernames.get(message.sender) is None:
                user = UserHelper.get_user(message.sender)
                if user is not None:
                    usernames[message.sender] = user['username']
                else:
                    usernames[message.sender] = '-'
            messages.append({
                'id' : message.id,
                'username' : usernames[message.sender],
                'content' : message.content,
                'send_time' : date_to_string(message.send_time)
            })
        return messages
