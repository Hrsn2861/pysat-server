"""models for message
"""
from django.db import models

from utils import getdate_now
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
    def get_messages(user_1, user_2, page):
        """get messages between user_1 and user_2
        """
        chat_id = ChatHelper.get_chat(user_1, user_2)
        messages = []
        if chat_id:
            qs = Message.objects.filter(chat_id=chat_id, valid=True)
            qs = qs.order_by('-id')
            qs = qs[(page - 1) * 20 : page * 20]
            for message in qs:
                messages.append({
                    'sender' : message.sender,
                    'content' : message.content,
                    'send_time' : message.send_time
                })
        return messages
