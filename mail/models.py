"""models for mail
"""
from enum import Enum
from django.db import models
from utils import getdate_now, getdate_none

class Mail(models.Model):
    """Mail Model
    """
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    title = models.CharField(max_length=64)
    content = models.TextField()
    quote = models.IntegerField()
    send_time = models.DateTimeField()
    read_time = models.DateTimeField()
    valid = models.BooleanField()

    class Meta:
        verbose_name = 'mail'
        verbose_name_plural = 'mails'
        get_latest_by = 'id'

class MailSearchParam(Enum):
    """some param for MailHelper.get_filter
    """
    SystemBox = 1
    MyInBox = 2
    MyOutBox = 3

    ReadMail = 1
    UnreadMail = 2
    AllMail = 3

class MailHelper:
    """Mail Helper for pysat-server

    It contains some functions about mail operation.
    """

    @staticmethod
    def send_mail(user_from, user_to, title, content):
        """send a mail into user_to's mailbox
        """
        if not isinstance(user_from, int) or not isinstance(user_to, int):
            return False
        if user_from == user_to:
            return False
        if not isinstance(title, str) or not isinstance(content, str):
            return False
        Mail(
            from_id=user_from,
            to_id=user_to,
            title=title,
            content=content,
            send_time=getdate_now(),
            read_time=getdate_none(),
            valid=True).save()
        return True

    @staticmethod
    def get_title(mail_id):
        """Get mail by id
        """
        if not isinstance(mail_id, int):
            return None
        mails = Mail.objects.filter(id=mail_id, valid=True)
        if mails.exists():
            mail = mails.last()
            return {
                'id' : mail.id,
                'title' : mail.title
            }
        return None

    @staticmethod
    def get_mail(mail_id):
        """Get mail by id
        """
        if not isinstance(mail_id, int):
            return None
        mails = Mail.objects.filter(id=mail_id, valid=True)
        if mails.exists():
            mail = mails.last()
            if mail.read_time == getdate_none():
                mail.read_time = getdate_now()
                mail.save()
            return {
                'id' : mail.id,
                'from' : mail.from_id,
                'to' : mail.to_id,
                'title' : mail.title,
                'content' : mail.content,
                'quote' : MailHelper.get_title(mail_id),
                'send_time' : mail.send_time,
                'read_time' : mail.read_time
            }
        return None

    @staticmethod
    def del_mail(mail_id):
        """delete mail by id
        """
        if not isinstance(mail_id, int):
            return None
        mails = Mail.objects.filter(id=mail_id, valid=True)
        for mail in mails:
            mail.valid = False
            mail.save()
        return None

    @staticmethod
    def get_filter(user_id, mail_type, mail_folder):
        """get filter for `get_mailcount` and `get_mailbox`
        """
        ret = {}
        if mail_type is MailSearchParam.SystemBox:
            ret['from'] = 0
            ret['to'] = user_id
        elif mail_type is MailSearchParam.MyInBox:
            ret['from__gt'] = 0
            ret['to'] = user_id
        elif mail_type is MailSearchParam.MyOutBox:
            ret['from'] = user_id
        else:
            ret['from'] = -1
        if mail_folder is MailSearchParam.AllMail:
            pass
        elif mail_folder is MailSearchParam.ReadMail:
            ret['read_time__gt'] = getdate_none()
        elif mail_folder is MailSearchParam.UnreadMail:
            ret['read_time'] = getdate_none()
        else:
            ret['read_time__lt'] = getdate_none()
        return ret

    @staticmethod
    def get_mailcount(user_id, mail_type, mail_folder):
        """Get mail count in mailbox
        """
        params = MailHelper.get_filter(user_id, mail_type, mail_folder)
        qs = Mail.objects.filter(**params)
        return qs.count()

    @staticmethod
    def get_mailbox(user_id, mail_type, mail_folder, page):
        """Get mailbox
        """
        if not isinstance(page, int):
            return []
        params = MailHelper.get_filter(user_id, mail_type, mail_folder)
        qs = Mail.objects.filter(**params)
        qs = qs.order_by('-id')
        mails = qs[(page - 1) * 20 : page * 20]
        ret = []
        for mail in mails:
            read_time = mail.read_time
            if read_time == getdate_none():
                read_time = None
            ret.append({
                'id' : mail.id,
                'from' : mail.from_id,
                'to' : mail.to_id,
                'title' : mail.title,
                'send_time' : mail.send_time,
                'read_time' : read_time,
            })
        return ret
