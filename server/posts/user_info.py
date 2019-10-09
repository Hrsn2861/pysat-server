from django.http import HttpResponse
import json

import server.model_utils.user as User
import server.model_utils.entrylog as Entrylog


def user_info(request):

    target_user = None
    
    if request.method == 'GET':
        key = request.GET.get('key')
        target_username = request.GET.get("username")
        log = Entrylog.getEntryLogByKey(key)

        # test
        target_username = 'Xianyu'
        log = {
            "userid" : 59
        }

        if log is None:
            status = 0
            msg = 'User logged out'

        else:            
            userid = log['userid']                                  #这个是用户的id            
            user = User.getUser(userid)                             #用户

            if user is None:
                msg = 'User login error'
                status = 0
            
            else:
                target_user = User.getUserByName(target_username)

                if target_user is None:
                    msg = 'User not found' 
                    
                else:
                    if(user["id"] == target_user["id"]):
                        target_user["id"] = 0
                    else:
                        pass
                    msg = 'User found'
    
    else:
        status = 0
        msg = 'Invalid request'
        status = 0
    
    data = {
        'status': status,
        'msg': msg,
        'user': target_user
    }
    return HttpResponse(json.dumps(data))
