from django.shortcuts import render
from django.http import HttpResponse
import json

from server.models import User

def check_login(request):
    pass

def login(request):

    # phonenumber = request.POST.get("phonenumber")
    # password = request.POST.get("password")

    data = {
        'status' : 1,
        'msg' : 'I am stupid.'
    }

    return HttpResponse(json.dumps(data))

def sign_up(request):

    data = {
        'status' : 1,
        'msg' : 'nothing wrong!'
    }

    return HttpResponse(json.dumps(data))