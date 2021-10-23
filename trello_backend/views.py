from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def homePageView(request, msg='0'):
    res = HttpResponse(msg.upper())
    res["Access-Control-Allow-Origin"] = "*"
    return res
