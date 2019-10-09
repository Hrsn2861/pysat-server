from django.http import HttpResponse
import json

import server.model_utils.user as User
import server.model_utils.entrylog as Entrylog

def user_info(request):

    target_user = None
    status = 0
    
    if request.method == 'GET':
        key = request.GET.get('entrykey')
        target_username = request.GET.get("username")

        if key is not None:
            log = Entrylog.getEntryLogByKey(key)
        else:
            log = None
            msg = 'Failed to get entry key'

        if log is None:
            status = 0
            if msg is None:
                msg = 'User logged out'

        else:            
            userid = log['userid']                                  #这个是用户的id            
            user = User.getUser(userid)                             #用户

            if user is None:
                msg = 'User login error'
                status = 0
            
            else:
                if target_username is not None:
                    target_user = User.getUserByName(target_username)
                    
                else:
                    target_user = None
                    msg = "Failed to get username"

                if target_user is None:
                    status = 0
                    if msg is None:
                        msg = 'User not found' 

                else:
                    status = 1
                    del target_user["password"]

                    if(user["id"] == target_user["id"]):
                        target_user["id"] = 0
                    else:
                        pass
                    msg = 'User found'
    
    else:
        status = 0
        msg = 'Invalid request'
    
    data = {
        'status': status,
        'msg': msg,
        'user': target_user
    }
    return HttpResponse(json.dumps(data))
