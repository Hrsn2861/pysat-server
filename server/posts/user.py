from django.shortcuts import render
from django.http import HttpResponse
import json

from server.models import User
from server.model_utils.user import getUser, getUserByName, getUserByTelphone, UserInfoChecker
from server.model_utils.entrylog import getEntryLogByKey

def check_login(request):
    msg = None
    if request.method == 'GET':
        key = request.GET.get('entry-key')
        if key is not None:
            log = getEntryLogByKey(str(key))
        else:
            log = None
            if msg is None:
                msg = "Failed to get entry-key"

        if log is not None:
            user = getUser(log['userid'])
        else:
            user = None
            if msg is None:
                msg = "Invalid entry-key"
        
        if user is not None:
            data = {
                'status' : 1,
                'user' : user
            }
        else:
            data = {
                'status' : 0,
                'user' : None
            }
            if msg is None:
                msg = "Invalid entry-key"
    else:
        data = {
            'status' : -1,
            'user' : None
        }
        if msg is None:
            msg = "Invalid request"

    data['msg'] = msg
    return HttpResponse(json.dumps(data))


def login(request):
    # phonenumber = request.GET.get("phonenumber")
    # password = request.GET.get("password")

    data = {
        'status' : 1,
        'msg' : 'I am stupid.'
    }

    return HttpResponse(json.dumps(data))


def sign_up(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        email = request.GET.get('email')
        telphone = request.GET.get('telphone')
        realname = request.GET.get('realname')
        school = request.GET.get('school')
        permission = 1

        if username is None or getUserByName(username) is not None:
            data = {
                'status' : 0,
                'msg' : "Invalid username"
            }
        elif telphone is None or getUserByTelphone(telphone) is not None or UserInfoChecker.check_telphone(telphone) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid telphone number"
            }
        elif password is None or UserInfoChecker.check_password(password) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid password"
            }
        elif email is None or UserInfoChecker.check_email(email) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid email address"
            }
        elif realname is None or UserInfoChecker.check_realname(realname) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid realname"
            }
        elif school is None or UserInfoChecker.check_school(school) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid school"
            }
        else:
            data = {
                'status' : 1,
                'msg' : "Check"
            }
        
    else:
        data = {
            'status' : -1,
            'msg' : "Invalid request"
        }

    return HttpResponse(json.dumps(data))