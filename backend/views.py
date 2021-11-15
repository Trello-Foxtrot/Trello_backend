from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from backend.models import User

import json


@csrf_exempt
def login(request):
    user = User()
    user.email = request.POST.get('email')
    user.password = request.POST.get('password')

    data = {}
    if User.objects.filter(email=user.email).filter(password=user.password):
        data['email'] = ''
    else:
        data['email'] = "User doesn't exists or given password is wrong"

    res = JsonResponse(data)
    res['Access-Control-Allow-Origin'] = '*'
    return res


@csrf_exempt
def sign_up(request):
    user = User()
    user.email = request.POST.get('email')
    user.password = request.POST.get('password')

    data = {}
    if not User.objects.filter(email=user.email):
        user.save()
        data['email'] = ''
    else:
        data['email'] = 'User already exists'

    res = JsonResponse(data)
    res['Access-Control-Allow-Origin'] = '*'
    return res

