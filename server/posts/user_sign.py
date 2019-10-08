from django.shortcuts import render
from django.http import HttpResponse
import json

import server.model_utils.user as User
import server.model_utils.entrylog as EntryLog

def check_login(request):
    msg = None
    if request.method == 'GET':
        key = request.GET.get('entrykey')
        print(key)
        if key is not None:
            log = EntryLog.getEntryLogByKey(str(key))
        else:
            log = None
            if msg is None:
                msg = "Failed to get entry key"

        if log is not None:
            user = User.getUser(log['userid'])
        else:
            user = None
            if msg is None:
                msg = "Invalid entry key"
        
        if user is not None:
            del user['password']
            data = {
                'status' : 1,
                'user' : user
            }
            msg = "Checked"
        else:
            data = {
                'status' : 0,
                'user' : None
            }
            if msg is None:
                msg = "Invalid entry key"
    else:
        data = {
            'status' : -1,
            'user' : None
        }
        if msg is None:
            msg = "Invalid request"

    data['msg'] = msg
    return HttpResponse(json.dumps(data))


def signin(request):
    if request.method == 'GET':
        identity = request.GET.get('identity')
        password = request.GET.get('password')

        user = User.getUserByName(identity)
        if user is None:
            user = User.getUserByTelphone(identity)
        if user is None:
            data = {
                'status' : 0,
                'msg' : "Invalid username or telphone"
            }
        elif password is None:
            data = {
                'status' : 0,
                'msg' : "Invalid password"
            }
        else:
            userid = user['id']
            if User.signin(userid, password):
                data = {
                    'status' : 1,
                    'msg' : EntryLog.addEntryLog(userid)
                }
            else:
                data = {
                    'status' : 0,
                    'msg' : "Password error"
                }
        
    else:
        data = {
            'status' : -1,
            'msg' : "Invalid request"
        }

    return HttpResponse(json.dumps(data))


def signup(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        email = request.GET.get('email')
        telphone = request.GET.get('telphone')
        realname = request.GET.get('realname')
        school = request.GET.get('school')

        if username is None or User.getUserByName(username) is not None:
            data = {
                'status' : 0,
                'msg' : "Invalid username"
            }
        elif telphone is None or User.getUserByTelphone(telphone) is not None or User.UserInfoChecker.check_telphone(telphone) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid telphone number"
            }
        elif password is None or User.UserInfoChecker.check_password(password) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid password"
            }
        elif email is None or User.UserInfoChecker.check_email(email) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid email address"
            }
        elif realname is None or User.UserInfoChecker.check_realname(realname) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid realname"
            }
        elif school is None or User.UserInfoChecker.check_school(school) is not True:
            data = {
                'status' : 0,
                'msg' : "Invalid school"
            }
        else:
            userid = User.signup(username=username, password=password, email=email, telphone=telphone, realname=realname, school=school, permission=1)
            user = User.getUser(userid)
            if user is not None:
                data = {
                    'status' : 1,
                    'msg' : "Sign up success"
                }
            else:
                data = {
                    'status' : -1,
                    'msg' : "Unknown Error"
                }
        
    else:
        data = {
            'status' : -1,
            'msg' : "Invalid request"
        }

    return HttpResponse(json.dumps(data))