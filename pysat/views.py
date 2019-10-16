"""Some simple pages here.
"""

from django.http import HttpResponse

from utils.request import get_ip

# Create your views here.

def test(request):
    """
    Test for mainpage.
    """
    print(get_ip(request))
    return HttpResponse("Test Success")
