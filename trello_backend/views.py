from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def homePageView(request, msg='0'):
    msg = msg.upper()
    return HttpResponse(msg)
