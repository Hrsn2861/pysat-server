"""Some simple pages here.
"""

from django.http import HttpResponse

# Create your views here.

def test(request):
    """
    Test for mainpage.
    """
    return HttpResponse("Test Success")
