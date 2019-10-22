"""views for mail
"""

import utils.response as Response

from utils.params import ParamType
from mail.models import MailHelper
from user.models.user import UserHelper

def mail_show(package):
    """this is the request of mail show
    """
    params = package.get('params')
    mail_id = params.get(ParamType.MailId)
    mail = MailHelper.get_mail(mail_id)

    if mail is None:
        return Response.error_response('No Email')

    from_user = UserHelper.get_user(int(mail['from']))
    to_user = UserHelper.get_user(int(mail['to']))

    if from_user is None:
        return Response.error_response('Sender Missing')
    if to_user is None:
        return Response.error_response('Reciever Missing')

    info = {
        'title' : mail['title'],
        'content' : mail['content'],
        'sender'  : from_user['username'],
        'reciever' : to_user['username'],
        'sendtime' : mail['send_time'],
        'read_time' : mail['read_time']
    }

    data = {
        'mail' : info
    }
    return Response.success_response(data)
