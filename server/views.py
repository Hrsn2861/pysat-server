from django.shortcuts import render
from django.http import HttpResponse

from server.models import User

# Create your views here.

def test_database(request):
    # add user
    # User(username="lightning", password="hello world", email="xxx@xxx.xxx", realname="Chen Xu", school="THU", permission=5).save()
    # User(username="hrsn", password="I am stupid.", email="xxx@xxx.xxx", realname="Chen Haozhan", school="THU", permission=1).save()

    # find and modify user
    # for user in User.objects.filter(username="hrsn"):
    #    user.password = "I am strong!"
    #    user.save()

    # delete user
    # User.objects.filter(username='temp').delete()

    return HttpResponse("Docker Success")