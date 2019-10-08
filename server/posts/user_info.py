from django.http import HttpResponse
import json

import server.model_utils.user as User

def user_info(request):
    if request.method == 'GET':
        pass

    return